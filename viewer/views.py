from django.shortcuts import render
from .models import Photo


def homepage(request):
    photos = Photo.objects.all()
    return render(request, 'homepage.html', {'photos': photos})


def reservations(request):
    return render(request, 'reservations.html')


def contact(request):
    return render(request, 'contact.html')