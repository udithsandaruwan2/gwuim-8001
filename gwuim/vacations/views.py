from django.shortcuts import render, redirect
from datetime import date
import calendar
from .models import Vacation
from .utils import get_prev_next_month
from .forms import VacationForm
from django.contrib import messages


def vacations(request, year=None, month=None):
    page = 'vacations'
    page_title = 'Vacations'
    profile = request.user.profile if request.user.is_authenticated else None
    today = date.today()
    # Use URL parameters for year and month if available, else fall back to today's date
    if not year or not month:
        year, month = today.year, today.month

    # When 'prev' or 'next' is clicked, capture the updated year and month
    if request.GET.get("year") and request.GET.get("month"):
        try:
            year = int(request.GET["year"])
            month = int(request.GET["month"])
        except ValueError:
            message = "Invalid date format. Please use YYYY-MM."
            return render(request, "vacations/vacations.html", {"error": message})

    print(f"Year: {year}, Month: {month}")  # Debug log to verify the updated values

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    vac_qs = Vacation.objects.filter(date__year=year, date__month=month)
    vac_set = {vd.date.day: vd for vd in vac_qs}

    prev_month, prev_year, next_month, next_year = get_prev_next_month(month, year)
    
    if request.method == "POST":
        form = VacationForm(request.POST)

        # Get values from the form manually if needed
        date_str = request.POST.get("date_")
        day_title = request.POST.get("day_title")  # Adjust field name to match your form's input field name

        try:
            Vacation.objects.create(
                date=date_str,
                title=day_title,
            )
            messages.success(request, "Vacation added successfully!")
            return redirect("vacations")  # Redirect to the vacations page
        except Exception as e:
            messages.error(request, f"Error adding vacation: {str(e)}")
            return redirect("vacations")

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_days': month_days,
        'vacation_days': vac_set,
        'day_names': ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        'today': today,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year
    }

    return render(request, "vacations/vacations.html", context)


