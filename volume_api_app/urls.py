from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import VolumeAPIViewSet
from volume_api_app.views.geotiffviews import GeoTIFFFileViewSet
from volume_api_app.views.demviews import DEMFileViewSet
from volume_api_app.views.derivedmeshview import (
    GLBMeshViewSet,
    OBJMeshViewSet,
    PointCloudMeshViewSet,
    PLYMeshViewSet,
)

router = DefaultRouter()
router.register(r"volume", VolumeAPIViewSet, basename="volume")
router.register(r"geotiffs", GeoTIFFFileViewSet, basename="geotiff")
router.register(r"glbmeshes", GLBMeshViewSet, basename="glbmesh")
router.register(r"dems", DEMFileViewSet, basename="dem")
router.register(r"objmeshes", OBJMeshViewSet, basename="objmesh")
router.register(r"pointcloudmeshes", PointCloudMeshViewSet, basename="pointcloudmesh")
router.register(r"plymeshes", PLYMeshViewSet, basename="plymesh")

urlpatterns = [
    path("", include(router.urls)),
]
