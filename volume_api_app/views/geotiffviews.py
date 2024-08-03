import math
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import parsers
from django.conf import settings
from ..models import GeoTIFFFile
from ..serializers.serializers import GeoTIFFFileSerializer
from geo.Geoserver import Geoserver
import requests
from django.http import HttpResponse

GEOSERVER_URL = settings.GEOSERVER_URL
GEOSERVER_USERNAME = settings.GEOSERVER_USERNAME
GEOSERVER_PASSWORD = settings.GEOSERVER_PASSWORD
GEOSERVER_GEOTIFF_WORKSPACE = settings.GEOSERVER_GEOTIFF_WORKSPACE


class GeoTIFFFileViewSet(viewsets.ModelViewSet):
    queryset = GeoTIFFFile.objects.all()
    serializer_class = GeoTIFFFileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(
        detail=False,
        methods=["post"],
        url_path="upload",
        parser_classes=[parsers.MultiPartParser, parsers.FormParser],
    )
    def upload_geotiff(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            geotiff_file = serializer.save()
            file_path = geotiff_file.file.path
            layer_name = geotiff_file.name

            geo = Geoserver(
                GEOSERVER_URL, username=GEOSERVER_USERNAME, password=GEOSERVER_PASSWORD
            )

            # Check if the layer already exists
            if not self.get_geotiff_layer(layer_name, GEOSERVER_GEOTIFF_WORKSPACE):
                try:
                    geo.create_workspace(workspace=GEOSERVER_GEOTIFF_WORKSPACE)
                except Exception:
                    pass

                geo.create_coveragestore(
                    layer_name=str(layer_name),
                    path=str(file_path),
                    workspace=GEOSERVER_GEOTIFF_WORKSPACE,
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_geotiff_layer(self, name, workspace=None):
        geo = Geoserver(
            GEOSERVER_URL, username=GEOSERVER_USERNAME, password=GEOSERVER_PASSWORD
        )

        if workspace is None:
            workspace = GEOSERVER_GEOTIFF_WORKSPACE

        try:
            layer = geo.get_layer(layer_name=name, workspace=workspace)
            if layer:
                return True
            else:
                return False
        except Exception:
            return False

    def tile_bbox(self, zoom, x, y):
        return {
            "north": self.tile_lat(y, zoom),
            "south": self.tile_lat(y + 1, zoom),
            "west": self.tile_lon(x, zoom),
            "east": self.tile_lon(x + 1, zoom),
        }

    def tile_lon(self, x, z):
        return x / math.pow(2.0, z) * 360.0 - 180

    def tile_lat(self, y, z):
        return math.degrees(
            math.atan(math.sinh(math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)))
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="tiles/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)",
    )
    def get_tile(self, request, pk=None, z=None, x=None, y=None):
        geotiff = self.get_object()
        layer_name = geotiff.name

        try:
            z = int(z)
            x = int(x)
            y = int(y)
        except ValueError:
            return Response(
                {"detail": "Invalid tile coordinates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bbox = self.tile_bbox(z, x, y)

        # Define the WMS request parameters
        params = {
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "layers": f"{GEOSERVER_GEOTIFF_WORKSPACE}:{layer_name}",
            "styles": "",
            "format": "image/png",
            "transparent": "true",
            "width": "250",
            "height": "250",
            "bbox": f"{bbox['west']},{bbox['south']},{bbox['east']},{bbox['north']}",
        }

        # Make the request to GeoServer
        response = requests.get(
            f"{GEOSERVER_URL}/wms",
            params=params,
            auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD),
        )

        if response.status_code == 200:
            return HttpResponse(response.content, content_type="image/png")
        else:
            return Response(
                {"detail": "Error fetching tile from GeoServer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
