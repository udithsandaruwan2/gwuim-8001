from django import template
from attendance_management.models import Attendance  # Adjust the import as necessary

register = template.Library()

@register.filter
def get_record_for_day(records, day):
    try:
        return records.get(date=day)  # Assuming each record has a unique date
    except Attendance.DoesNotExist:
        return None