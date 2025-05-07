from django.shortcuts import render
from datetime import date, timedelta
import calendar
from calendar import monthrange
from datetime import datetime
from .models import Vacation

def vacations(request, year=None, month=None):
    page = 'vacations'
    page_title = 'Vacations'

    profile = request.user.profile if request.user.is_authenticated else None

    

    today = date.today()
    year  = year  or today.year
    month = month or today.month

    # get a matrix of weeks; each week is a list of 7 ints (0 means no day)
    cal = calendar.Calendar(firstweekday=6)  # Sunday=6, Monday=0; adjust as needed
    month_days = cal.monthdayscalendar(year, month)

    # pull vacation days for this month
    vac_qs = Vacation.objects.filter(date__year=year, date__month=month)
    vac_set = {vd.date.day: vd for vd in vac_qs}




    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "month_days": month_days,
        "vacation_days": vac_set,
        "day_names": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        "today": date.today(),
    }
    return render(request, 'vacations/vacations.html', context)



