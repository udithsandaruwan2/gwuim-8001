from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Attendance
from datetime import datetime

def searchAttendance(request):
    search_query = request.GET.get('search', '').strip()
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    attendance = Attendance.objects.all()

    # Filter by employee_id if numeric
    if search_query.isdigit():
        attendance = attendance.filter(employee_id=search_query)
    elif search_query:
        attendance = Attendance.objects.none()  # Invalid search query

    # Filter by date range if both dates are provided
    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            attendance = attendance.filter(date__range=(from_date_obj, to_date_obj))
        except ValueError:
            attendance = Attendance.objects.none()  # Invalid date format

    return attendance, search_query, from_date, to_date


def paginateAttendance(request, attendance, results):
    page = request.GET.get('page')
    paginator = Paginator(attendance, results)

    try:
        attendance = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        attendance = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        attendance = paginator.page(page)

    left_index = max(int(page) - 1, 1)
    right_index = min(int(page) + 2, paginator.num_pages + 1)

    custom_range = range(left_index, right_index)
    return custom_range, attendance

