from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from .utils import searchAttendance, paginateAttendance

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
