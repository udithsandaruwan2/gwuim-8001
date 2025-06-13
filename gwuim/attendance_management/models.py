from django.db import models
import uuid

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('leave', 'Leave'),
        ('pending', 'Pending'),
    ]
    employee_id = models.IntegerField(null=True, blank=True)  # Store employee ID from API
    date = models.DateField(null=True, blank=True)  # Store date of attendance  
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # Additional fields can be added as needed, e.g., for leave types, reasons, etc.
    is_late = models.BooleanField(default=False)  # To track if the employee is late
    is_early = models.BooleanField(default=False)  # To track if the employee leaves early
    is_short_leave = models.BooleanField(default=False)  # To track if the employee takes a short leave
    is_half_day_leave = models.BooleanField(default=False)  # To track if the employee takes a half day
    
    # Common fields
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically determine status before saving
        if self.check_in and self.check_out:
            self.status = "present"
        else:
            self.status = "pending"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['employee_id', 'date']

    def __str__(self):
        return f"{self.employee_id} - {self.date} - {self.status}"
