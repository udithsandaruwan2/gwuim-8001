from django import template
from django import template
from attendance_management.models import Attendance  # Adjust the import as necessary


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_dic_item(dictionary, key):
    key = str(key).lower()
    if isinstance(dictionary, dict):  # Ensure it's a dictionary
        return dictionary.get(key, 0)  # Default to 0 if key is missing
    return 0  # Return 0 if dictionary itself is None or invalid

@register.filter
def get_value(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)  # Display as an integer if no decimal part
    return value  # Display float with decimals if needed


register = template.Library()

@register.filter
def get_record_for_day(records, day):
    try:
        return records.get(date=day)  # Assuming each record has a unique date
    except Attendance.DoesNotExist:
        return None

from django import template
register = template.Library()

