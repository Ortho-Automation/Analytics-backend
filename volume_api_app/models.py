from django.db import models
import os


def get_geotiff_file_path(instance, filename):
    return os.path.join("Data", "geotiffs", filename)


class GeoTIFFFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_geotiff_file_path)


def get_glb_file_path(instance, filename):
    return os.path.join("Data", "glb", filename)


class GLBMesh(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_glb_file_path)

    def __str__(self):
        return self.name
