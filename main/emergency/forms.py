from django import forms
from .models import EmergencyRequest

class EmergencyRequestForm(forms.ModelForm):
    class Meta:
        model = EmergencyRequest
        fields = ['phone_number', 'note', 'latitude', 'longitude', 'city']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'note': forms.Textarea(attrs={'placeholder': 'Brief note (optional)', 'rows': 2}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }
