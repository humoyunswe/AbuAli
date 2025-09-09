from .models import Candidates
from django import forms


class CandadiateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'portfolio', 'github', 'linkedin', 'telegram']
        
        