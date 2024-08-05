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
    data_url = serializers.SerializerMethodField()

    class Meta:
        model = GLBMesh
        fields = ["id", "name", "file", "file_url", "data", "data_url"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.id)
        return obj.file.url

    def get_data_url(self, obj):
        request = self.context.get("request")
        if obj.data and hasattr(obj.data, "url"):
            return request.build_absolute_uri(f"/api/glbmeshes/{obj.id}")
        return None

    def create(self, validated_data):
        data_file = validated_data.pop("data", None)
        instance = super().create(validated_data)
        if data_file:
            instance.data.save(data_file.name, data_file)
        return instance


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
