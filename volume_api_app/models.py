from django.db import models
import os


def get_image_file_path(instance, filename):
    # Create the path for storing images
    return os.path.join("Data", "stored_data", filename)


class ImageFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_image_file_path)


class URLImageFile(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()


def get_geotiff_file_path(instance, filename):
    return os.path.join("Data", "geotiffs", filename)


class GeoTIFFFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_geotiff_file_path)
