from django import forms
from .models import Vacation

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ['date', 'title']
