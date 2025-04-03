# forms.py
from django import forms
from .models import AttendanceFile

class AttendanceFileForm(forms.ModelForm):
    class Meta:
        model = AttendanceFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control mt-2 edit-input',
            }),
        }
