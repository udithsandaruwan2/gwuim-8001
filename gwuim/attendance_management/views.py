from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def attendanceRecords(request):
    page = 'attendance_rcecords'
    page_title = 'Attendance Records'

    profile = request.user.profile

    # employees, search_query = searchEmployees(request)
    # custom_range, employees = paginateEmployees(request, employees, 10)

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile
    }
    return render(request, 'attendance_management/attendance-records.html', context)
