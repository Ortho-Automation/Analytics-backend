from django.contrib import admin
from .models import ImageFile, URLImageFile


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")


@admin.register(URLImageFile)
class URLImageFileAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
