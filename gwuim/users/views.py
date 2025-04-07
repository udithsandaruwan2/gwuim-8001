from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db import models
import calendar
from datetime import datetime
from audit_logs.utils import create_audit_log
from attendance_management.models import Attendance
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import calendar


def home(request):
    """Home page view."""
    page = 'home'
    page_title = 'Home'

    try:
        profile = request.user.profile  # Get user profile if available
    except:
        profile = None

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile
    }
    return render(request, 'users/index.html', context)


def login(request):
    """Login view for user authentication."""
    page = 'login'
    page_title = 'Login'

    try:
        profile = request.user.profile  # Get user profile if available
    except:
        profile = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Validate input
        if not username:
            messages.error(request, 'Username is required')
            return redirect('login')

        if not password:
            messages.error(request, 'Password is required')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Email or password is incorrect')
            return redirect('login')

        auth_login(request, user)

        # Log the action: User logged in successfully
        create_audit_log(
            action_performed="User Logged In",
            performed_by=user.profile,
            details=f"User {username} logged in."
        )

        messages.success(request, f'Welcome back, {user.username}!')
        return redirect('dashboard')

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile
    }
    return render(request, 'users/login-register.html', context)


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view for logged-in users."""
    page = 'dashboard'
    page_title = 'Dashboard'

    try:
        profile = request.user.profile  # Get user profile if available
    except:
        profile = None

    current_year = datetime.now().year
    current_month = datetime.now().strftime('%B')
    current_month_days = calendar.monthrange(current_year, datetime.now().month)[1]
    average_count = Attendance.objects.filter(date__year=current_year, date__month=datetime.now().month).count()
    average_count = average_count / current_month_days if current_month_days > 0 else 0

    # Log the action: User accessed the dashboard
    create_audit_log(
        action_performed="Accessed Dashboard",
        performed_by=profile,
        details="User accessed the dashboard page."
    )

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile, 
        'current_year': current_year,
        'current_month': current_month,
        'current_month_days': current_month_days,
        'average_count': average_count,
    }
    return render(request, 'users/dashboard.html', context)


@login_required(login_url='login')
def logoutView(request):
    """Logout view to log out the user."""
    user = request.user
    logout(request)

    # Log the action: User logged out
    create_audit_log(
        action_performed="User Logged Out",
        performed_by=user.profile,
        details=f"User {user.username} logged out."
    )

    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')




@login_required(login_url='login')
def attendance_chart_data(request):
    """View to fetch and return attendance data for the chart."""
    year = int(request.GET.get('year', datetime.now().year))  # Default to current year

    # Log the action
    create_audit_log(
        action_performed="Accessed Attendance Chart Data",
        performed_by=request.user.profile,
        details=f"User accessed attendance chart data for the year {year}."
    )

    # Generate a dictionary with all months initialized to 0
    monthly_data = {f"{month} {year}": 0 for month in calendar.month_name[1:]}

    # Query attendance data grouped by month
    data = (
        Attendance.objects
        .filter(date__year=year)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_present=Count('uid', filter=models.Q(status='present')))
        .order_by('month')
    )

    # Fill in the data
    for entry in data:
        month_str = entry['month'].strftime('%B %Y')
        monthly_data[month_str] = entry['total_present']

    # Format for chart
    chart_data = {
        'labels': list(monthly_data.keys()),
        'values': list(monthly_data.values()),
    }

    return JsonResponse(chart_data)

@login_required(login_url='login')
def attendance_pie_chart_data(request):
    """View to fetch and return attendance pie chart data."""

    create_audit_log(
        action_performed="Accessed Attendance Pie Chart Data",
        performed_by=request.user.profile,
        details="User accessed attendance pie chart data."
    )

    data = {
        'labels': ['Present', 'Leave', 'Pending'],
        'values': [
            Attendance.objects.filter(status='present').count(),
            Attendance.objects.filter(status='leave').count(),
            Attendance.objects.filter(status='pending').count(),
        ]
    }

    return JsonResponse(data)
