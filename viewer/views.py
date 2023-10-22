from django.shortcuts import render
from .models import Photo
from reservation.models import Reservation


def homepage(request):
    photos = Photo.objects.all()
    return render(request, 'homepage.html', {'photos': photos})


def reservations(request):
    event_data = []
    all_reservations = Reservation.objects.all()
    for reservation in all_reservations:
        event = {
            'start': reservation.date_from.strftime('%Y-%m-%d'),
            'end': reservation.date_to.strftime('%Y-%m-%d')
        }
        event_data.append(event)

    context = {
        'reservations': reservations,
        'event_data': event_data
    }
    return render(request, 'reservations.html', context)


def contact(request):
    return render(request, 'contact.html')

