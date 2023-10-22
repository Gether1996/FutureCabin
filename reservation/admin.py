from django.contrib import admin
from .models import Reservation, Order


@admin.register(Reservation)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to')


@admin.register(Order)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name_surname', 'id', 'date_from', 'date_to', 'email', 'address', 'city', 'postal')
