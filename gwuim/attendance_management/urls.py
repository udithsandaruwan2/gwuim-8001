from django.urls import path
from . import views

urlpatterns = [
    path('attendance-records/', views.attendanceRecords, name='attendance_records'),
]