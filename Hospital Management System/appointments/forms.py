# appointments/forms.py
from django import forms
from .models import Availability
# appointments/forms.py
from datetime import datetime

class AvailabilityForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_t = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    end_t = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = Availability
        fields = ['emergency_note', 'emergency_start', 'emergency_end','max_patients']
        widgets = {
            'emergency_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for emergency status'}),
            'emergency_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'emergency_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'max_patients': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'e.g. 10'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_t = cleaned_data.get('start_t')
        end_t = cleaned_data.get('end_t')

        if date and start_t and end_t:
            # This will now work with the correct import
            cleaned_data['start_time'] = datetime.combine(date, start_t)
            cleaned_data['end_time'] = datetime.combine(date, end_t)
        return cleaned_data