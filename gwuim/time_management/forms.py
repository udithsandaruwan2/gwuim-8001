# forms.py

from django import forms
from .models import EmployeeWorkSchedule
import requests
from gwuim.settings import API_BASE_URL

class EmployeeWorkScheduleForm(forms.ModelForm):
    employee_title = forms.ChoiceField(
        choices=[],
        required=True,
        label="Employee Title"
    )
    employee_title_uid = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = EmployeeWorkSchedule
        fields = [
            'employee_title',        # stores title name
            'employee_title_uid',    # stores title UID
            'official_start', 'official_end',
            'relief_start', 'relief_end',
            'late_in_start', 'late_in_end',
            'covering_start', 'covering_end',
            'short_leave_morning_start', 'short_leave_morning_end',
            'short_leave_evening_start', 'short_leave_evening_end',
            'half_leave_morning_start', 'half_leave_morning_end',
            'half_leave_evening_start', 'half_leave_evening_end',
        ]
        widgets = {
            key: forms.TimeInput(attrs={'type': 'time'})
            for key in [
                'official_start', 'official_end',
                'relief_start', 'relief_end',
                'late_in_start', 'late_in_end',
                'covering_start', 'covering_end',
                'short_leave_morning_start', 'short_leave_morning_end',
                'short_leave_evening_start', 'short_leave_evening_end',
                'half_leave_morning_start', 'half_leave_morning_end',
                'half_leave_evening_start', 'half_leave_evening_end',
            ]
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.uid_map = {}  # map title → uid

        try:
            response = requests.get(f'{API_BASE_URL}titles/', timeout=5)
            response.raise_for_status()
            titles = response.json()
            if isinstance(titles, list):
                choices = []
                for title in titles:
                    choices.append((title['title'], title['title']))  # title as both value and label
                    self.uid_map[title['title']] = title['uid']
                self.fields['employee_title'].choices = [('', 'Select Title')] + choices
            else:
                self.fields['employee_title'].choices = [('', 'Invalid title list')]
        except Exception:
            self.fields['employee_title'].choices = [('', 'Error loading titles')]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("employee_title")

        # Set UID based on selected title using self.uid_map
        if title in self.uid_map:
            cleaned_data["employee_title_uid"] = self.uid_map[title]
        else:
            cleaned_data["employee_title_uid"] = ""

        return cleaned_data
