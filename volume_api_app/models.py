from django.db import models
import os


def get_file_path(instance, filename, folder):
    return os.path.join("Data", folder, filename)


def get_json_path(instance, filename, folder):
    if filename is None:
        return
    else:
        return os.path.join("Data", f"{folder}json", filename)


# Define specific path functions for each model type
def get_geotiff_file_path(instance, filename):
    return get_file_path(instance, filename, "geotiffs")


def get_glb_file_path(instance, filename):
    return get_file_path(instance, filename, "glb")


def get_glb_json_path(instance, filename):
    return get_json_path(instance, filename, "glb")


def get_dem_file_path(instance, filename):
    return get_file_path(instance, filename, "dems")


def get_obj_file_path(instance, filename):
    return get_file_path(instance, filename, "obj")


def get_obj_json_path(instance, filename):
    return get_json_path(instance, filename, "obj")


def get_pointcloud_file_path(instance, filename):
    return get_file_path(instance, filename, "pointcloud")


def get_pointcloud_json_path(instance, filename):
    return get_json_path(instance, filename, "pointcloud")


def get_ply_file_path(instance, filename):
    return get_file_path(instance, filename, "ply")


def get_ply_json_path(instance, filename):
    return get_json_path(instance, filename, "ply")


class BaseMesh(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=None)  # This will be set in derived classes
    data = models.FileField(
        upload_to=None, blank=True, null=True
    )  # This will be set in derived classes

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class GeoTIFFFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_geotiff_file_path)

    @property
    def geoserver(self):
        template = "geotiff/wms?service=WMS&version=1.1.0&request=GetMap&layers=geotiff%3A{name}&bbox={{bbox-epsg-3857}}&width=256&height=256&srs=EPSG:3857&styles=&format=image/png&transparent=true"
        return template.format(name=self.name)

    def __str__(self):
        return self.name


class GLBMesh(BaseMesh):
    file = models.FileField(upload_to=get_glb_file_path)
    data = models.FileField(upload_to=get_glb_json_path, blank=True, null=True)

    class Meta:
        verbose_name = "GLB Mesh"
        verbose_name_plural = "GLB Meshes"


class DEMFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_dem_file_path)

    @property
    def geoserver(self):
        template = "dem/wms?service=WMS&version=1.1.0&request=GetMap&layers=dem%3A{name}&bbox={{bbox-epsg-3857}}&width=256&height=256&srs=EPSG:3857&styles=&format=image/png&transparent=true"
        return template.format(name=self.name)

    def __str__(self):
        return self.name


class OBJMesh(BaseMesh):
    file = models.FileField(upload_to=get_obj_file_path)
    data = models.FileField(upload_to=get_obj_json_path, blank=True, null=True)

    class Meta:
        verbose_name = "OBJ Mesh"
        verbose_name_plural = "OBJ Meshes"


class PointCloudMesh(BaseMesh):
    file = models.FileField(upload_to=get_pointcloud_file_path)
    data = models.FileField(upload_to=get_pointcloud_json_path, blank=True, null=True)

    class Meta:
        verbose_name = "Point Cloud Mesh"
        verbose_name_plural = "Point Cloud Meshes"


class PLYMesh(BaseMesh):
    file = models.FileField(upload_to=get_ply_file_path)
    data = models.FileField(upload_to=get_ply_json_path, blank=True, null=True)

    class Meta:
        verbose_name = "PLY Mesh"
        verbose_name_plural = "PLY Meshes"
