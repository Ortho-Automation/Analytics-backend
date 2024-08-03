from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import VolumeAPIViewSet
from volume_api_app.views.views import ImageFileDetailViewSet
from volume_api_app.views.geotiffviews import GeoTIFFFileViewSet

router = DefaultRouter()
router.register(r"volume", VolumeAPIViewSet, basename="volume")
router.register(r"image-file", ImageFileDetailViewSet)
router.register(r"geotiffs", GeoTIFFFileViewSet, basename="geotiff")

urlpatterns = [
    path("", include(router.urls)),
]
