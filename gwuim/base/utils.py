from vacations.models import Vacation
from attendance_management.models import Attendance
from csv_manager.utils import get_days_in_month

def getLeavesPerMonth(id, year):
    attendance = Attendance.objects.filter(employee_id=id, date__year=year)

    leave_count = [0] * 12

    for month in range(1, 13):
        # Get all days in the selected month
        total_days_in_month = get_days_in_month(year, month)

        # Get attendance records for the month
        records = attendance.filter(date__month=month).order_by('date')

        Vacations = Vacation.objects.filter(date__month=month).order_by('date')

        for date_ in total_days_in_month:
            # Check if the date is in the records
            if date_ not in records.values_list('date', flat=True):

                if date_ not in Vacations.values_list('date', flat=True):
                    # If the date is a vacation, set status to "Vacation"
                    leave_count[month-1] += 1
    
    return leave_count
            

