from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import LeaveBalanceSerializer, VacationSerializer, LeaveCountSerializer
from rest_framework.response import Response
from vacations.models import Vacation
from .utils import getLeavesPerMonth, getAttendanceCountperMonth, getOtherLeavesCount
from rest_framework import serializers
from audit_logs.utils import create_audit_log

@api_view(['GET'])
def getRoutes(request):
    """View to display available API routes."""
    routes = [
        'api/vacations/',
        'api/employees/<str:employee_id>/<int:year>/',
        'api/employees/<str:employee_id>/<int:year>/<int:month>/',
        'api/employees/<str:employee_id>/<int:year>/<int:month>/other-leaves/',
    ]
    create_audit_log(
        action_performed="Viewed API Routes",
        performed_by=request.user.profile if request.user.is_authenticated else None,
        details="User viewed the API routes."
    )
    return Response(routes)



@api_view(['GET'])
def getLeaveCount(request, employee_id, year):
    """View to retrieve leave count for a specific employee."""
    leave_count = getLeavesPerMonth(employee_id, year)
    data = leave_count
    create_audit_log(
        action_performed="Retrieved Leave Count",
        performed_by=request.user.profile if request.user.is_authenticated else None,
        details=f"User retrieved leave count for employee {employee_id} for {year}."
    )
    return Response(data)

@api_view(['GET'])
def getVacationDetails(request):
    """View to retrieve details of a specific employee."""
    vacations = Vacation.objects.all()
    serializer = VacationSerializer(vacations, many=True)
    create_audit_log(
        action_performed="Viewed Vacation Details",
        performed_by=request.user.profile if request.user.is_authenticated else None,
        details="User viewed vacation details."
    )
    return Response(serializer.data)

@api_view(['GET'])
def getAttendanceCount(request, employee_id, year, month):
    """View to retrieve attendance count for a specific employee."""
    # Assuming you have a function to get attendance count
    attendance_count = getAttendanceCountperMonth(employee_id, year, month)
    data = attendance_count
    create_audit_log(
        action_performed="Retrieved Attendance Count",
        performed_by=request.user.profile if request.user.is_authenticated else None,
        details=f"User retrieved attendance count for employee {employee_id} for {month}/{year}."
    )
    return Response(data)

@api_view(['GET'])
def getOtherLeaveCountDetails(request, employee_id, year, month):
    """View to retrieve other leave count for a specific employee."""
    other_leave_count = getOtherLeavesCount(employee_id, year, month)
    serializer = LeaveBalanceSerializer(other_leave_count, many=True)
    create_audit_log(
        action_performed="Retrieved Other Leave Count",
        performed_by=request.user.profile if request.user.is_authenticated else None,
        details=f"User retrieved other leave count for employee {employee_id} for {month}/{year}."
    )
    return Response(serializer.data)