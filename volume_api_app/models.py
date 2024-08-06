from django.db import models
import os


def get_geotiff_file_path(instance, filename):
    return os.path.join("Data", "geotiffs", filename)


class GeoTIFFFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_geotiff_file_path)

    @property
    def geoserver(self):
        # URL template
        template = "geotiff/wms?service=WMS&version=1.1.0&request=GetMap&layers=geotiff%3A{name}&bbox={{bbox-epsg-3857}}&width=256&height=256&srs=EPSG:3857&styles=&format=image/png&transparent=true"
        return template.format(name=self.name)

    def __str__(self):
        return self.name


def get_glb_file_path(instance, filename):
    return os.path.join("Data", "glb", filename)


def get_glb_json_path(instance, filename):
    if filename is None:
        return
    else:
        return os.path.join("Data", "glbjson", filename)


class GLBMesh(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_glb_file_path)
    data = models.FileField(upload_to=get_glb_json_path, blank=True, null=True)

    def __str__(self):
        return self.name


# New DEM model
def get_dem_file_path(instance, filename):
    return os.path.join("Data", "dems", filename)


class DEMFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_dem_file_path)

    @property
    def geoserver(self):
        # URL template
        template = "dem/wms?service=WMS&version=1.1.0&request=GetMap&layers=dem%3A{name}&bbox={{bbox-epsg-3857}}&width=256&height=256&srs=EPSG:3857&styles=&format=image/png&transparent=true"
        return template.format(name=self.name)

    def __str__(self):
        return self.name
