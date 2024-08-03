from rest_framework import serializers
from ..models import ImageFile, URLImageFile, GeoTIFFFile


class CoordinateField(serializers.ListField):
    child = serializers.FloatField()


class PolygonField(serializers.ListField):
    child = CoordinateField()


class PolygonSerializer(serializers.Serializer):
    polygons = serializers.ListField(child=PolygonField())


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = "__all__"


class URLImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLImageFile
        fields = "__all__"


class GeoTIFFFileSerializer(serializers.ModelSerializer):
    tile_url = serializers.SerializerMethodField()

    class Meta:
        model = GeoTIFFFile
        fields = ["id", "name", "file", "tile_url"]

    def get_tile_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/geotiffs/{obj.id}/get-tile/")
        return f"/api/geotiffs/{obj.id}/get-tile/"
