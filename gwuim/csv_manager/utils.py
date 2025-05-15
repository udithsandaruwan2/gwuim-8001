import csv
from datetime import datetime
import os
from datetime import time as dtime 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from attendance_management.models import Attendance  # Adjust with your actual app name

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

        # for row in reader:
        #     employee_id = row["AC-No."].strip()
        #     timestamp_str = row["Time"].strip()
        #     new_state = row["New State"].strip()
        #     exception = row["Exception"].strip()

        #     # # Skip invalid records
        #     # if exception == "Invalid" or exception != "FOT":
        #     #     continue

        #     # Convert timestamp to date and time
        #     timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %H:%M")
        #     date = timestamp.date()
        #     time = timestamp.time()

        #     # Unique key for each employee per day
        #     record_key = (employee_id, date)

        #     # Check if the record exists in our dictionary
        #     if record_key not in attendance_records:
        #         attendance_records[record_key] = {
        #             "employee_id": employee_id,
        #             "date": date,
        #             "check_in": None,
        #             "check_out": None,
        #         }

        #     # Assign check-in or check-out based on New State
        #     if "OverTime In" in new_state:
        #         attendance_records[record_key]["check_in"] = time
        #     elif "OverTime Out" in new_state:
        #         attendance_records[record_key]["check_out"] = time





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




    # Save to the database
    for key, data in attendance_records.items():
        attendance, created = Attendance.objects.get_or_create(
            employee_id=data["employee_id"],
            date=data["date"],
            defaults={"check_in": data["check_in"], "check_out": data["check_out"]},
        )

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
