from datetime import timedelta
from django.shortcuts import render
from .models import Photo
from reservation.models import Order


def homepage(request):
    photos = Photo.objects.all()
    event_data = []
    all_reservations = Order.objects.all()
    for reservation in all_reservations:
        event = {
            'start': reservation.date_from.strftime('%Y-%m-%d'),
            'end': (reservation.date_to + timedelta(days=1)).strftime('%Y-%m-%d')
        }
        event_data.append(event)

    context = {
        'event_data': event_data,
        'photos': photos
    }

    return render(request, 'homepage.html', context)