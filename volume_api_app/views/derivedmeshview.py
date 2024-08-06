from ..models import GLBMesh, OBJMesh, PointCloudMesh, PLYMesh
from ..serializers.serializers import (
    GLBMeshSerializer,
    OBJMeshSerializer,
    PointCloudMeshSerializer,
    PLYMeshSerializer,
)
from .meshview import BaseMeshViewSet


class GLBMeshViewSet(BaseMeshViewSet):
    queryset = GLBMesh.objects.all()
    serializer_class = GLBMeshSerializer

    def get_content_type(self):
        return "model/gltf-binary"


class OBJMeshViewSet(BaseMeshViewSet):
    queryset = OBJMesh.objects.all()
    serializer_class = OBJMeshSerializer

    def get_content_type(self):
        return "model/obj"


class PointCloudMeshViewSet(BaseMeshViewSet):
    queryset = PointCloudMesh.objects.all()
    serializer_class = PointCloudMeshSerializer

    def get_content_type(self):
        return "model/pointcloud"


class PLYMeshViewSet(BaseMeshViewSet):
    queryset = PLYMesh.objects.all()
    serializer_class = PLYMeshSerializer

    def get_content_type(self):
        return "model/ply"
