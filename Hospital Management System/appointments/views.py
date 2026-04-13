from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Availability
from .forms import AvailabilityForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.conf import settings

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor: return redirect('patient_dashboard')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            # Use the combined times from our clean() method
            slot.start_time = form.cleaned_data['start_time']
            slot.end_time = form.cleaned_data['end_time']
            slot.save()
            return redirect('doctor_dashboard')
    else:
        form = AvailabilityForm()

    slots = Availability.objects.filter(doctor=request.user).order_by('start_time')
    return render(request, 'appointments/doctor_dashboard.html', {'form': form, 'slots': slots})


@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('doctor_dashboard')

    # Fetch all availability slots that are NOT booked
    # We use select_related to get the doctor's info efficiently
    available_slots = Availability.objects.filter(is_booked=False).select_related('doctor').order_by('start_time')

    return render(request, 'appointments/patient_dashboard.html', {
        'slots': available_slots
    })

@login_required
def book_appointment(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(Availability, id=slot_id)
        
        # 1. Check if there is still room
        if not slot.is_full:
            slot.current_bookings += 1
            
            # If we hit the limit, mark as booked so it hides from the patient list
            if slot.is_full:
                slot.is_booked = True 
                
            slot.save()
            
            # 2. ONLY send email if booking was successful
            subject = f'Confirmed: Appointment with {slot.doctor.username}'
            message = (
                f"Hello {request.user.username},\n\n"
                f"Your appointment is confirmed for {slot.start_time.strftime('%A, %B %d')}.\n"
                f"Time: {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}.\n\n"
                f"Doctor: {slot.doctor.username}\n"
                f"Location: Main Hospital Wing\n\n"
                "Please arrive 10 minutes early."
            )
            recipient_list = [request.user.email] 
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                messages.success(request, f"Appointment booked! Confirmation sent to {request.user.email}")
            except Exception as e:
                messages.warning(request, "Appointment booked, but email failed to send.")
                print(f"Email Error: {e}")
        
        else:
            # If someone tried to book a slot that just became full
            messages.error(request, "Sorry, this doctor's limit for this slot has been reached.")

        return redirect('patient_dashboard')
    
    return redirect('patient_dashboard')

@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('doctor_dashboard')

    # IMPORTANT: Filter out slots that are marked as is_booked (Full)
    available_slots = Availability.objects.filter(is_booked=False).select_related('doctor').order_by('start_time')

    return render(request, 'appointments/patient_dashboard.html', {'slots': available_slots})