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
    # Common fields
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Employee Work Schedule"
        verbose_name_plural = "Employee Work Schedules"

    def __str__(self):
        return f"{self.employee_title}'s schedule"

