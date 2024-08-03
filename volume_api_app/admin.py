from django.contrib import admin
from .models import GeoTIFFFile


@admin.register(GeoTIFFFile)
class GeoTIFFFileAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
