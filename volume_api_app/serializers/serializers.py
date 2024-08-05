# serializers/serializers.py

from rest_framework import serializers
from ..models import GeoTIFFFile, GLBMesh, DEMFile


class CoordinateField(serializers.ListField):
    child = serializers.FloatField()


class PolygonField(serializers.ListField):
    child = CoordinateField()


class PolygonSerializer(serializers.Serializer):
    polygons = serializers.ListField(child=PolygonField())
    id = serializers.IntegerField(required=False)


class GeoTIFFFileSerializer(serializers.ModelSerializer):
    tile_url = serializers.SerializerMethodField()

    class Meta:
        model = GeoTIFFFile
        fields = ["id", "name", "file", "tile_url"]

    def get_tile_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/geotiffs/{obj.id}/tiles/")
        return f"/api/geotiffs/{obj.id}/tiles/"


class GLBMeshSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = GLBMesh
        fields = ["id", "name", "file", "file_url"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.id)
        return obj.file.url


# New DEMFileSerializer
class DEMFileSerializer(serializers.ModelSerializer):
    tile_url = serializers.SerializerMethodField()

    class Meta:
        model = DEMFile
        fields = ["id", "name", "file", "tile_url"]

    def get_tile_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/dems/{obj.id}/tiles/")
        return f"/api/dems/{obj.id}/tiles/"
