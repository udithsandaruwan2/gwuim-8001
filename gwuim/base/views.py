from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import VacationSerializer, LeaveCountSerializer
from rest_framework.response import Response
from vacations.models import Vacation
from .utils import getLeavesPerMonth, getAttendanceCountperMonth
from rest_framework import serializers

@api_view(['GET'])
def getRoutes(request):
    """View to display available API routes."""
    routes = [
        'api/vacations/',
        'api/employees/<str:employee_id>/<int:year>/',
        'api/employees/<str:employee_id>/<int:year>/<int:month>/',
    ]
    return Response(routes)



@api_view(['GET'])
def getLeaveCount(request, employee_id, year):
    """View to retrieve leave count for a specific employee."""
    leave_count = getLeavesPerMonth(employee_id, year)
    data = leave_count

    return Response(data)

@api_view(['GET'])
def getVacationDetails(request):
    """View to retrieve details of a specific employee."""
    vacations = Vacation.objects.all()
    serializer = VacationSerializer(vacations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAttendanceCount(request, employee_id, year, month):
    """View to retrieve attendance count for a specific employee."""
    # Assuming you have a function to get attendance count
    attendance_count =getAttendanceCountperMonth(employee_id, year, month)
    data = attendance_count
    return Response(data)