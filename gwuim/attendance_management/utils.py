from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Attendance

def searchAttendance(request):
    search_query = request.GET.get('search', '').strip()
    
    if search_query.isdigit():  # Ensure search_query is a number before filtering by employee_id
        attendance = Attendance.objects.filter(employee_id=search_query)
    else:
        attendance = Attendance.objects.none()  # Return empty queryset if invalid input

    return attendance, search_query


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

