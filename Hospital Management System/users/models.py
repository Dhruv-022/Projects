# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # These flags will help in redirecting the user after login
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({'Doctor' if self.is_doctor else 'Patient'})"