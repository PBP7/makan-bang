from django.shortcuts import render
from datetime import datetime  # Import datetime
import calendar  # Import calendar


def meal_planning(request):
    # Mendapatkan tanggal saat ini
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Mendapatkan hari-hari dalam bulan
    month_days = calendar.monthcalendar(current_year, current_month)

    # Nama bulan
    month_name = today.strftime('%B')

    context = {
        'month_name': month_name,
        'month_days': month_days,
        'current_day': today.day
    }

    return render(request, 'meal_planning.html', context)
