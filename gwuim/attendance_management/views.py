from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from .utils import searchAttendance, paginateAttendance, searchAttendanceSingle, paginateAttendanceSingle
import requests

@login_required(login_url='login')
def attendanceRecords(request):
    page = 'attendance_rcecords'
    page_title = 'Attendance Records'

    profile = request.user.profile

    attendance, search_query, from_date, to_date = searchAttendance(request)
    custom_range, attendance = paginateAttendance(request, attendance, 10)
    

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
        'attendance': attendance,
        'search_query': search_query,
        'custom_range': custom_range,
        'from_date': from_date,
        'to_date': to_date,
        
    }
    return render(request, 'attendance_management/attendance-records.html', context)

@login_required(login_url='login')
def attendanceRecordsSingle(request, pk):
    page = 'attendance_rcecords_single'
    page_title = 'Attendance Records'

    profile = request.user.profile

    attendance, from_date, to_date = searchAttendanceSingle(request, pk)
    custom_range, attendance = paginateAttendanceSingle(request, attendance, 10)
    

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
        'attendance': attendance,
        'custom_range': custom_range,
        'from_date': from_date,
        'to_date': to_date,
        
    }
    return render(request, 'attendance_management/attendance-records-single.html', context)

API_BASE_URL = 'http://localhost:8000/api/'

def employees(request):
    response = requests.get(f'{API_BASE_URL}employees/')
    employees = response.json()
    context = {
        'employees': employees,
    }
    return render(request, 'attendance_management/employees.html', context)