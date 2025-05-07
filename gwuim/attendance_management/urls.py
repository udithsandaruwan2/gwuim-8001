from django.urls import path
from . import views

urlpatterns = [
    path('attendance-records/', views.attendanceRecords, name='attendance_records'),
    path('attendance-records/<str:pk>/', views.attendanceRecordsSingle, name='attendance_records_single'),
    path('employees/', views.employees, name='employees'),
    path('api/employees/', views.getEmployees, name='get_employees'),

]