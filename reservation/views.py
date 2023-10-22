from django.shortcuts import render, redirect
from .models import Reservation
from datetime import datetime, timedelta
from django.contrib import messages


def checkout(request):
    if request.user:
        user = request.user
    dates = request.GET.get('dates')

    if not dates:
        messages.error(request, 'Vyberte si termín.')
        return redirect('reservations')

    dates = dates.split(',')
    selected_dates_by_user = []
    reserved_dates = []

    if len(dates) == 1:
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[0], '%Y-%m-%d')
    else:
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[1], '%Y-%m-%d')
        if end_date < start_date:
            start_date = datetime.strptime(dates[1], '%Y-%m-%d')
            end_date = datetime.strptime(dates[0], '%Y-%m-%d')

    while start_date <= end_date:
        selected_dates_by_user.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)

    if len(selected_dates_by_user) <3:
        messages.error(request, 'Vyberte si minimálne 2 noci.')
        return redirect('reservations')

    # Retrieve all reservations from the database
    reservations = Reservation.objects.all()

    # Iterate through reservations to extract reserved dates
    # last day of reservation can be reserved again
    for reservation in reservations:
        start_date = reservation.date_from
        end_date = reservation.date_to - timedelta(days=1)

        # Generate a list of dates within the reservation range
        while start_date <= end_date:
            reserved_dates.append(start_date.strftime('%Y-%m-%d'))
            start_date += timedelta(days=1)

    for date in selected_dates_by_user:
        if date in reserved_dates:
            messages.error(request, 'Váš termín je už obsadený.')
            return redirect('reservations')

    return render(request, 'checkout.html', {'dates': selected_dates_by_user})
