from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from .utils import searchAttendance, paginateAttendance, searchAttendanceSingle, paginateAttendanceSingle
import requests
from django.http import JsonResponse

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


def employees(request):
    page = 'employees'
    page_title = 'Employees'

    profile = request.user.profile

    
    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
    }
    return render(request, 'attendance_management/employees.html', context)


API_BASE_URL = 'http://localhost:8000/api/'  # replace with your actual base URL

def getEmployees(request):
    try:
        response = requests.get(f'{API_BASE_URL}employees/', timeout=5)
        response.raise_for_status()  # raise exception for 4xx/5xx responses

        employees = response.json()

        # Optional: Validate the structure if needed
        if not isinstance(employees, list):
            return JsonResponse({'message': 'Unexpected response format from API.'}, status=500)

        return JsonResponse(employees, safe=False, status=200)

    except requests.exceptions.Timeout:
        return JsonResponse({'message': 'The request timed out. Please try again later.'}, status=504)

    except requests.exceptions.ConnectionError:
        return JsonResponse({'message': 'Failed to connect to the API server.'}, status=503)

    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({'message': f'API returned an error: {str(http_err)}'}, status=response.status_code)

    except ValueError:
        return JsonResponse({'message': 'Invalid JSON response from API.'}, status=500)

    except Exception as e:
        return JsonResponse({'message': f'An unexpected error occurred: {str(e)}'}, status=500)
