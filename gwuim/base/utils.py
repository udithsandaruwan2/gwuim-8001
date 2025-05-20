from vacations.models import Vacation
from attendance_management.models import Attendance
from csv_manager.utils import get_days_in_month
from calendar import monthrange
from datetime import datetime

def getLeavesPerMonth(employee_id, year):
    # Filter only present days
    attendance_present = Attendance.objects.filter(
        employee_id=employee_id, 
        date__year=year
    ).values_list('date', flat=True).order_by('date')

    # All vacation dates in the year
    vacation_dates = Vacation.objects.filter(
        date__year=year
    ).values_list('date', flat=True).order_by('date')

    # Convert to datetime.datetime for comparison
    attendance_present_set = set(datetime.combine(d, datetime.min.time()) for d in attendance_present)
    vacation_dates_set = set(datetime.combine(d, datetime.min.time()) for d in vacation_dates)

    leave_count = [0] * 12

    for month in range(1, 13):
        days_in_month = get_days_in_month(year, month)  # Returns list of datetime.datetime
        for current_loop_date in days_in_month:
            if current_loop_date not in attendance_present_set:
                if current_loop_date not in vacation_dates_set:
                    leave_count[month - 1] += 1

        if not any(date.month == month for date in attendance_present_set):
            leave_count[month - 1] = 0

    return leave_count




def get_days_in_month(year, month):
    """Helper function to get all dates in a given month."""
    num_days = monthrange(year, month)[1]
    return [datetime(year, month, day) for day in range(1, num_days + 1)]

def getAttendanceCountperMonth(employee_id, year, month):
    # Get attendance records for the employee for the specified month
    attendance_present = Attendance.objects.filter(
        employee_id=employee_id,
        date__year=year,
        date__month=month
    ).values_list('date', flat=True)

    # Get vacation dates for the given year
    vacation_dates = Vacation.objects.filter(
        date__year=year
    ).values_list('date', flat=True)

    # Convert to datetime.date sets for quick lookup
    attendance_present_set = set(attendance_present)
    vacation_dates_set = set(vacation_dates)

    # Count days the employee was present and it's not a vacation day
    attendance_count = sum(
        1 for day in attendance_present_set if day not in vacation_dates_set
    )

    return attendance_count
