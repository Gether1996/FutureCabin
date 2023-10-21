from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_from', 'date_to')
