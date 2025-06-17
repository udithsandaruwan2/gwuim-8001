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

def process_attendance_csv(file_path):
    """
    Reads a CSV file and processes attendance data while ensuring one record per employee per day.
    """
    attendance_records = {}  # Dictionary to hold unique records per employee per day

    if file_path.startswith('/media/'):
        file_path = file_path[len('/media/'):]

    # Construct the absolute file path using MEDIA_ROOT
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # Ensure the file exists
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    with open(full_path, newline='', encoding='utf-8') as csvfile:
        sample = csvfile.read(1024)  # Read a sample for detection
        csvfile.seek(0)  # Reset file position
        dialect = csv.Sniffer().sniff(sample)
        reader = csv.DictReader(csvfile, dialect=dialect)

        print("Detected Delimiter:", dialect.delimiter)



        for row in reader:
            employee_id = row["AC-No."].strip()
            timestamp_str = row["Time"].strip()
            exception = row["Exception"].strip()

            # Convert timestamp to date and time
            timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %H:%M")
            date = timestamp.date()
            time_only = timestamp.time()

            # Unique key for each employee per day
            record_key = (employee_id, date)

            # Check if the record exists in our dictionary
            if record_key not in attendance_records:
                attendance_records[record_key] = {
                    "employee_id": employee_id,
                    "date": date,
                    "check_in": None,
                    "check_out": None,
                }

            # Manual time-based logic: before or at 12:30 → check-in, after → check-out
            if time_only <= dtime(12, 30) and attendance_records[record_key]["check_in"] is None:
                attendance_records[record_key]["check_in"] = time_only
            elif time_only > dtime(12, 30) and attendance_records[record_key]["check_out"] is None:
                attendance_records[record_key]["check_out"] = time_only



    employee_list = getEmployeeList()
    title_list = getTitleList()
    employee_work_schedule = EmployeeWorkSchedule.objects.all()
    # Save to the database
    for key, data in attendance_records.items():
        attendance, created = Attendance.objects.get_or_create(
            employee_id=data["employee_id"],
            date=data["date"],
            defaults={"check_in": data["check_in"], "check_out": data["check_out"]},
        )

        
        employee_data = next((item for item in employee_list if item['employee_code'] == data["employee_id"]), None)
        if employee_data['title_uid']:
            title_data = next((item for item in title_list if item['uid'] == employee_data['title_uid']), None)
            schedule_data = next((item for item in employee_work_schedule if item.employee_title_uid == employee_data['title_uid']), None)
            if schedule_data:
                if data["check_in"] and schedule_data.official_start and data["check_in"] > schedule_data.official_start:
                    #late
                    attendance.is_late = True
                    attendance.is_early = False
                    if not schedule_data.relief_start <= data["check_in"] <= schedule_data.relief_end:
                    #late but not also within relief period
                        if schedule_data.late_in_start <= data["check_in"] <= schedule_data.late_in_end:
                        #late but within late in period
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['late_count'] != 0:
                                get_or_create_leave_balance['late_count'] -= 1
                            elif get_or_create_leave_balance['short_leave_balance'] != 0:
                                get_or_create_leave_balance['short_leave_balance'] -= 1
                                get_or_create_leave_balance['leave_type'] = 'short'
                            else:
                                attendance.is_half_day = True
                                get_or_create_leave_balance['leave_type'] = 'half'
                                get_or_create_leave_balance['half_leave_count'] += 1
                            get_or_create_leave_balance.save()
                        elif schedule_data.short_leave_morning_start <= data["check_in"] <= schedule_data.short_leave_morning_end:
                            #short leave morning
                            attendance.is_short_leave = True
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['short_leave_balance'] != 0:
                                get_or_create_leave_balance['short_leave_balance'] -= 1
                                get_or_create_leave_balance['leave_type'] = 'short'
                            else:
                                attendance.is_half_day = True
                                get_or_create_leave_balance['leave_type'] = 'half'
                                get_or_create_leave_balance['half_leave_count'] += 1
                            get_or_create_leave_balance.save()
                        elif schedule_data.half_leave_morning_start <= data["check_in"] <= schedule_data.half_leave_morning_end:
                            #half leave morning
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                                
                            )
                            if get_or_create_leave_balance['half_leave_count'] != 0:
                                get_or_create_leave_balance['half_leave_count'] += 1
                                get_or_create_leave_balance['leave_type'] = 'half'
                            get_or_create_leave_balance.save()
                elif data["check_in"] and schedule_data.late_in_start and data["check_in"] <= schedule_data.late_in_start:
                    #on time
                    attendance.is_late = False
                    attendance.is_early = True
                else:
                    if not data["check_out"] and schedule_data.official_end and data["check_out"] >= schedule_data.official_end:
                        #early leave
                        if schedule_data.short_leave_evening_start <= data["check_out"] <= schedule_data.short_leave_evening_end:
                            #short leave evening
                            attendance.is_short_leave = True
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['late_count_covered'] < 3 and not get_or_create_leave_balance['late_count_covered'] != 2:
                                get_or_create_leave_balance['late_count_covered'] += 1
                            get_or_create_leave_balance.save()

        # If record already exists, update check-in or check-out
        if not created:
            if data["check_in"]:
                attendance.check_in = data["check_in"]
            if data["check_out"]:
                attendance.check_out = data["check_out"]

        # Set status
        attendance.status = "Present" if attendance.check_in and attendance.check_out else "Pending"
        attendance.save()

    print("Attendance data processed successfully!")

import calendar
from datetime import datetime, timedelta

def get_days_in_month(year, month):
    # Get the number of days in the month
    _, num_days = calendar.monthrange(year, month)
    
    # Generate a list of date objects for each day of the month
    days_in_month = [datetime(year, month, day) for day in range(1, num_days + 1)]
    return days_in_month

