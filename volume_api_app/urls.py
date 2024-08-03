from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import VolumeAPIViewSet
from volume_api_app.views.geotiffviews import GeoTIFFFileViewSet
from volume_api_app.views.glbmeshviews import GLBMeshViewSet

router = DefaultRouter()
router.register(r"volume", VolumeAPIViewSet, basename="volume")
router.register(r"geotiffs", GeoTIFFFileViewSet, basename="geotiff")
router.register(
    r"glbmeshes", GLBMeshViewSet, basename="glbmesh"
)  # Register the GLBMeshViewSet

urlpatterns = [
    path("", include(router.urls)),
]
