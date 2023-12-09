from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from .models import Photo
from reservation.models import Order
from django.utils.translation import activate


def homepage(request):
    language_code = request.session.get('django_language', 'sk')
    activate(language_code)
    photos = Photo.objects.all()
    event_data = []
    all_reservations = Order.objects.all()

    for reservation in all_reservations:
        current_date = reservation.date_from
        end_date = reservation.date_to + timedelta(days=1)

        while current_date < end_date:
            event = {
                'start': current_date.strftime('%Y-%m-%d'),
                'end': current_date.strftime('%Y-%m-%d'),
                'classNames': 'in-between'  # Default class for days in between
            }
            if current_date == reservation.date_from:
                event['classNames'] = 'starting-day'
            if current_date == end_date - timedelta(days=1):
                event['classNames'] = 'finishing-day'

            event_data.append(event)
            current_date += timedelta(days=1)

    # Combine events for the same day
    combined_event_data = {}
    for event in event_data:
        date = event['start']
        if date in combined_event_data:
            combined_event_data[date]['classNames'] = 'in-between'
        else:
            combined_event_data[date] = event

    context = {
        'event_data': list(combined_event_data.values()),
        'photos': photos
    }

    return render(request, 'homepage.html', context)


def switch_language(request, language_code):
    if request.method == 'POST':
        activate(language_code)
        request.session['django_language'] = language_code
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})
