from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo')