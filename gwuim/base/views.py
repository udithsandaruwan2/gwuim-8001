from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import VacationSerializer
from rest_framework.response import Response
from vacations.models import Vacation

@api_view(['GET'])
def getRoutes(request):
    """View to display available API routes."""
    routes = [
        'api/vacations/',
        'api/employees/<str:pk>/',
    ]
    return Response(routes)

@api_view(['GET'])
def getVacationDetails(request):
    """View to retrieve details of a specific employee."""
    vacations = Vacation.objects.all()
    serializer = VacationSerializer(vacations, many=True)
    return Response(serializer.data)