import csv
from datetime import datetime
import os
from datetime import time as dtime 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from attendance_management.models import Attendance  # Adjust with your actual app name
from gwuim.settings import API_BASE_URL
import requests
from time_management.models import EmployeeWorkSchedule, LeaveBalance  # Adjust with your actual app name

def getTitleList():
    """
    Fetches the list of employee titles from the API.
    Returns a dictionary mapping title names to their UIDs.
    """
    try:
        response = requests.get(f'{API_BASE_URL}titles/', timeout=5)
        response.raise_for_status()
        titles = response.json()
        return titles
    except requests.RequestException as e:
        print(f"Error fetching titles: {e}")
    return {}

def getEmployeeList():
    """
    Fetches the list of employees from the API.
    Returns a dictionary mapping employee names to their UIDs.
    """
    try:
        response = requests.get(f'{API_BASE_URL}employees/', timeout=5)
        response.raise_for_status()
        employees = response.json()
        return employees
    except requests.RequestException as e:
        print(f"Error fetching employees: {e}")
    return {}

import calendar
from datetime import datetime, timedelta

def get_days_in_month(year, month):
    # Get the number of days in the month
    _, num_days = calendar.monthrange(year, month)
    
    # Generate a list of date objects for each day of the month
    days_in_month = [datetime(year, month, day) for day in range(1, num_days + 1)]
    return days_in_month




def process_attendance_csv(file_path):
    """
    Reads a CSV file and processes attendance data while ensuring one record per employee per day.
    """
    attendance_records = {}

    if file_path.startswith('/media/'):
        file_path = file_path[len('/media/'):]

    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    with open(full_path, newline='', encoding='utf-8') as csvfile:
        sample = csvfile.read(1024)
        csvfile.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        reader = csv.DictReader(csvfile, dialect=dialect)

        print("Detected Delimiter:", dialect.delimiter)

        for row in reader:
            employee_id = row["AC-No."].strip()
            timestamp_str = row["Time"].strip()
            exception = row["Exception"].strip()

            timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %H:%M")
            date = timestamp.date()
            time_only = timestamp.time()

            record_key = (employee_id, date)

            if record_key not in attendance_records:
                attendance_records[record_key] = {
                    "employee_id": employee_id,
                    "date": date,
                    "check_in": None,
                    "check_out": None,
                }

            if time_only <= dtime(12, 30) and attendance_records[record_key]["check_in"] is None:
                attendance_records[record_key]["check_in"] = time_only
            elif time_only > dtime(12, 30) and attendance_records[record_key]["check_out"] is None:
                attendance_records[record_key]["check_out"] = time_only

    employee_list = getEmployeeList()
    title_list = getTitleList()
    employee_work_schedule = EmployeeWorkSchedule.objects.all()

    for key, data in attendance_records.items():
        attendance, created = Attendance.objects.get_or_create(
            employee_id=data["employee_id"],
            date=data["date"],
            defaults={"check_in": data["check_in"], "check_out": data["check_out"]},
        )

        employee_data = next((e for e in employee_list if e['employee_code'] == attendance.employee_id), None)
        
        if employee_data and employee_data['title_uid']:
            leave_balance, _ = LeaveBalance.objects.get_or_create(
                            employee_id=employee_data['employee_code'],
                            year=data["date"].year,
                            month=data["date"].month
                        )
            # print("yes, we hace it" + employee_data['uid'])
            title_data = next((t for t in title_list if t['uid'] == employee_data['title_uid']), None)
            schedule_data = next((s for s in employee_work_schedule if s.employee_title_uid == employee_data['title_uid']), None)

            if schedule_data and data["check_in"]:
                if schedule_data.official_start and data["check_in"] > schedule_data.official_start:
                    attendance.is_late = True
                    attendance.is_early = False

                    if not schedule_data.relief_start <= data["check_in"] <= schedule_data.relief_end:
                        if schedule_data.late_in_start <= data["check_in"] <= schedule_data.late_in_end:
                            if leave_balance.late_count > 0:
                                leave_balance.late_count -= 1
                            elif leave_balance.short_leave_balance > 0:
                                leave_balance.short_leave_balance -= 1
                                attendance.is_short_leave = True
                            else:
                                leave_balance.half_leave_count += 1
                                attendance.is_half_day_leave = True
                            leave_balance.save()

                        elif schedule_data.short_leave_morning_start <= data["check_in"] <= schedule_data.short_leave_morning_end:
                            if leave_balance.short_leave_balance > 0:
                                leave_balance.short_leave_balance -= 1
                                attendance.is_short_leave = True
                            else:
                                leave_balance.half_leave_count += 1
                                attendance.is_half_day_leave = True
                            leave_balance.save()

                        elif schedule_data.half_leave_morning_start <= data["check_in"] <= schedule_data.half_leave_morning_end:
                            leave_balance.half_leave_count += 1
                            leave_balance.save()
                elif schedule_data.late_in_start and data["check_in"] <= schedule_data.late_in_start:
                    attendance.is_late = False
                    attendance.is_early = True

            if schedule_data and data["check_out"] and schedule_data.official_end and data["check_out"] < schedule_data.official_end:
                if schedule_data.short_leave_evening_start <= data["check_out"] <= schedule_data.short_leave_evening_end:
                    attendance.is_short_leave = True
                    leave_balance, _ = LeaveBalance.objects.get_or_create(
                        employee_id=employee_data['employee_code'],
                        year=data["date"].year,
                        month=data["date"].month
                    )
                    if leave_balance.short_leave_balance > 0:
                        leave_balance.short_leave_balance -= 1
                    else:
                        attendance.is_half_day_leave = True
                        leave_balance.half_leave_count += 1
            elif data["check_out"] and schedule_data.covering_end and data["check_out"] >= schedule_data.covering_end:
                leave_balance.late_count_covered += 1
            leave_balance.save()

        else:
            print(f"Employee data not found for ID: {data['employee_id']}")
            continue

        if not created:
            if data["check_in"]:
                attendance.check_in = data["check_in"]
            if data["check_out"]:
                attendance.check_out = data["check_out"]

        attendance.status = "present" if attendance.check_in and attendance.check_out else "pending"
        attendance.save()

    print("Attendance data processed successfully!")
