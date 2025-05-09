from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import VacationSerializer, LeaveCountSerializer
from rest_framework.response import Response
from vacations.models import Vacation
from .utils import getLeavesPerMonth
from rest_framework import serializers

@api_view(['GET'])
def getRoutes(request):
    """View to display available API routes."""
    routes = [
        'api/vacations/',
        'api/employees/<str:pk>/',
    ]
    return Response(routes)



@api_view(['GET'])
def getLeaveCount(request, employee_id, year):
    """View to retrieve leave count for a specific employee."""
    attendance_count, leave_count = getLeavesPerMonth(employee_id, year)
    data = {
        'attendance_count': attendance_count,
        'leave_count': leave_count,
    }
    return Response(data)

@api_view(['GET'])
def getVacationDetails(request):
    """View to retrieve details of a specific employee."""
    vacations = Vacation.objects.all()
    serializer = VacationSerializer(vacations, many=True)
    return Response(serializer.data)

