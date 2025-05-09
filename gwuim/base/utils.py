from vacations.models import Vacation
from attendance_management.models import Attendance
from csv_manager.utils import get_days_in_month

from datetime import datetime

def getLeavesPerMonth(employee_id, year):
    # Filter only present days
    attendance_present = Attendance.objects.filter(
        employee_id=employee_id, 
        date__year=year,
        status='present'
    ).values_list('date', flat=True).order_by('date')

    # All vacation dates in the year
    vacation_dates = Vacation.objects.filter(
        date__year=year
    ).values_list('date', flat=True).order_by('date')

    # Convert to datetime.datetime for comparison
    attendance_present_set = set(datetime.combine(d, datetime.min.time()) for d in attendance_present)
    vacation_dates_set = set(datetime.combine(d, datetime.min.time()) for d in vacation_dates)

    leave_count = [0] * 12
    attendance_count = [0] * 12

    for month in range(1, 13):
        days_in_month = get_days_in_month(year, month)  # Returns list of datetime.datetime
        for current_loop_date in days_in_month:
            if current_loop_date not in attendance_present_set:
                if current_loop_date not in vacation_dates_set:
                    leave_count[month - 1] += 1
            else:
                attendance_count[month - 1] += 1

    return attendance_count, leave_count  # Or return leave_count if needed