from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from .models import EmployeeWorkSchedule
from .forms import EmployeeWorkScheduleForm
import requests
from gwuim.settings import API_BASE_URL


def timeManagement(request):
    """
    Render the time management page with a list of work schedules.
    """
    page = 'title_schedules'
    page_title = 'Time Management'
    title_schedules = EmployeeWorkSchedule.objects.all()

    profile = request.user.profile if request.user.is_authenticated else None


    context = {
        'title_schedules': title_schedules,
        'page': page,
        'page_title': page_title,
        'profile': profile, 
    }
    return render(request, 'time_management/time_management.html', context)

def timeManagementAdd(request):
    """
    Render the time management page.
    """
    page = 'title_schedules'
    page_title = 'Time Management'
    form = EmployeeWorkScheduleForm()

    profile = request.user.profile if request.user.is_authenticated else None

    if request.method == 'POST':
        form = EmployeeWorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work schedule updated successfully.')
            return redirect('time_management')
        else:
            messages.error(request, 'Failed to update work schedule.')
            return redirect('time_management')
    context = {
        'form': form,
        'page': page,
        'page_title': page_title,
        'profile': profile,
    }
    return render(request, 'time_management/time_management_form.html', context)

def timeManagementUpdate(request, pk):
    """
    Render the time management page.
    """
    page = 'title_schedules'
    page_title = 'Time Management'
    title_schedule = EmployeeWorkSchedule.objects.get(uid=pk)
    form = EmployeeWorkScheduleForm(instance=title_schedule)

    profile = request.user.profile if request.user.is_authenticated else None

    if request.method == 'POST':
        form = EmployeeWorkScheduleForm(request.POST, instance=title_schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work schedule updated successfully.')
            return redirect('time_management')
        else:
            messages.error(request, 'Failed to update work schedule.')
            return redirect('time_management')
    context = {
        'form': form,
        'page': page,
        'page_title': page_title,
        'profile': profile,
    }

    return render(request, 'time_management/time_management_form.html', context)

def timeManagementDelete(request, pk):
    """
    Delete a work schedule.
    """
    page = 'title_schedules'
    page_title = 'Time Management'
    title_schedule = EmployeeWorkSchedule.objects.get(uid=pk)

    profile = request.user.profile if request.user.is_authenticated else None

    if request.method == 'POST':
        title_schedule.delete()
        messages.success(request, 'Work schedule deleted successfully.')
        return redirect('time_management')

    context = {
        'title_schedule': title_schedule,
        'page': page,
        'page_title': page_title,
        'profile': profile,
    }

    return render(request, 'dashboard/delete-confirmation.html', context)
