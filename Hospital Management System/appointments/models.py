from django.db import models
from django.conf import settings

# appointments/models.py
from django.db import models
from django.conf import settings

class Availability(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    emergency_note = models.CharField(max_length=255, blank=True, null=True)
    
    # New Fields for specific emergency hours
    emergency_start = models.TimeField(blank=True, null=True)
    emergency_end = models.TimeField(blank=True, null=True)

    #New fields for appointments tracking
    max_patients = models.PositiveIntegerField(default=1, help_text="How many patients can book this slot?")
    current_bookings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.doctor.username} | {self.start_time}"
    
    @property
    def is_full(self):
        return self.current_bookings >= self.max_patients

class Booking(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_patient': True}
    )
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} with {self.availability.doctor.username}"