from django.db import models
import uuid

class EmployeeWorkSchedule(models.Model):
    employee_title_uid = models.CharField(max_length=100, null=True, blank=True)
    employee_title = models.CharField(max_length=100, null=True, blank=True)

    # Official Work Period
    official_start = models.TimeField(null=True, blank=True)
    official_end = models.TimeField(null=True, blank=True)

    # Relief / Break Period
    relief_start = models.TimeField(null=True, blank=True)
    relief_end = models.TimeField(null=True, blank=True)

    # Late Arrival Grace Period
    late_in_start = models.TimeField(null=True, blank=True)
    late_in_end = models.TimeField(null=True, blank=True)

    # Covering Time (worked beyond official hours)
    covering_start = models.TimeField(null=True, blank=True)
    covering_end = models.TimeField(null=True, blank=True)

    # Short Leave Morning
    short_leave_morning_start = models.TimeField(null=True, blank=True)
    short_leave_morning_end = models.TimeField(null=True, blank=True)

    # Short Leave Evening
    short_leave_evening_start = models.TimeField(null=True, blank=True)
    short_leave_evening_end = models.TimeField(null=True, blank=True)

    # Half Leave Morning
    half_leave_morning_start = models.TimeField(null=True, blank=True)
    half_leave_morning_end = models.TimeField(null=True, blank=True)

    # Half Leave Evening
    half_leave_evening_start = models.TimeField(null=True, blank=True)
    half_leave_evening_end = models.TimeField(null=True, blank=True)

    # Common fields
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Employee Work Schedule"
        verbose_name_plural = "Employee Work Schedules"

    def __str__(self):
        return f"{self.employee_title}'s schedule"

class LeaveBalance(models.Model):
    TYPES = [
        ('short', 'Short Leave'),
        ('half', 'Half Day Leave')
    ]
    employee_id = models.IntegerField(null=True, blank=True)  # Store employee ID from API
    late_count = models.IntegerField(default=5, null=True, blank=True)  # Count of late arrivals
    late_count_covered = models.IntegerField(default=0, null=True, blank=True)  # Count of late arrivals covered
    is_late_covered_totally = models.BooleanField(default=False, null=True)  # Flag to indicate if late arrivals are covered
    leave_type = models.CharField(max_length=50, null=True, blank=True, choices=TYPES)  # Type of leave (e.g., sick, vacation)
    short_leave_balance = models.IntegerField(default=2, null=True, blank=True)  # Remaining short leave balance
    half_leave_count = models.IntegerField(default=0, null=True, blank=True)  # Remaining half leave count
    year = models.IntegerField(null=True, blank=True)  # Year for which the leave balance is applicable
    month = models.IntegerField(null=True, blank=True)  # Month for which the leave balance is applicable
    # Common fields
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leave Balance"
        verbose_name_plural = "Leave Balances"

    def save(self, *args, **kwargs):
        if self.late_count_covered >= 3:
            self.is_late_covered_totally = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Leave Balance for Employee {self.employee_id} - {self.leave_type}"