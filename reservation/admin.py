from django.contrib import admin
from .models import Order


@admin.register(Order)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name_surname', 'id', 'date_from', 'date_to', 'email', 'address', 'city', 'postal')
