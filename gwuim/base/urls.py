from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name="api"),
    path("vacations/", views.getVacationDetails, name="api_vacations"),
    path("employees/<str:employee_id>/<int:year>/", views.getLeaveCount, name="api_leave_count"),
    path("employees/<str:employee_id>/<int:year>/<int:month>/", views.getAttendanceCount, name="api_attendance_count"),
]