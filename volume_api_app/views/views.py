import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from volume_api_app.serializers.serializers import PolygonSerializer
from volume_api_app.mixins.volume_calculation_tool import (
    VolumeCalculationToolStandalone,
)
from shapely.geometry import Polygon
from ..models import DEMFile


class VolumeAPIViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        request_body=PolygonSerializer,
        responses={200: "OK"},
    )
    @action(detail=False, methods=["post"], url_path="computation")
    def computation(self, request):
        serializer = PolygonSerializer(data=request.data)
        if serializer.is_valid():
            polygons_data = serializer.validated_data.get("polygons", [])
            polygons = [Polygon(coords) for coords in polygons_data]

            dem_id = serializer.validated_data.get("id")
            if not dem_id:
                return Response(
                    {"error": "DEM file ID must be provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                dem = DEMFile.objects.get(id=dem_id)
                dem_path = dem.file.path
            except DEMFile.DoesNotExist:
                return Response(
                    {"error": "DEM file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            pixel_size_x = 0.07085796904697951037
            pixel_size_y = 0.07085530815116512782

            tool = VolumeCalculationToolStandalone()
            volumes = tool.calculate_volume_above_approx_base_level(
                dem_path, polygons, pixel_size_x, pixel_size_y
            )

            results = [
                {
                    "polygon_id": i + 1,
                    "volume_above_base_level": (
                        volume
                        if volume is not None
                        else "Input shapes do not overlap raster."
                    ),
                }
                for i, volume in enumerate(volumes)
            ]

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
