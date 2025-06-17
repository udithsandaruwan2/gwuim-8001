from django.contrib import admin
from .models import EmployeeWorkSchedule, LeaveBalance

admin.site.register(EmployeeWorkSchedule)
admin.site.register(LeaveBalance)