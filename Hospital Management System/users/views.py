# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm # We will create this next
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def dashboard_redirect(request):
    if request.user.is_doctor:
        return redirect('doctor_dashboard') # We'll define this URL in appointments app
    elif request.user.is_patient:
        return redirect('patient_dashboard') # We'll define this URL in appointments app
    else:
        # If somehow a user has no role, send to logout or home
        return redirect('login')