# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    #The "Common Interface" choice
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        username = self.cleaned_data.get('username')

        if role == 'doctor':
            user.is_doctor = True
            # SOPHISTICATED RENAMING LOGIC:
            # 1. Strip any existing "Dr." or "Dr " (case-insensitive)
            # 2. Add "Dr. " back exactly once at the start
            clean_name = username.replace('Dr.', '').replace('dr.', '').replace('Dr ', '').replace('dr ', '').strip()
            user.username = f"Dr.{clean_name}"
        elif role == 'patient':
            user.is_patient = True
        
        if commit:
            user.save()
        return user