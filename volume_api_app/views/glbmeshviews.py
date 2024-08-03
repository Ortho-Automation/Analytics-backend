from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import FileResponse
from ..models import GLBMesh
from ..serializers.serializers import GLBMeshSerializer
import logging
import os


class GLBMeshViewSet(viewsets.ModelViewSet):
    queryset = GLBMesh.objects.all()
    serializer_class = GLBMeshSerializer

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
    def upload_glb(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            glb_file = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="content-as-json")
    def content_as_json(self, request, pk=None):
        glb_mesh = self.get_object()
        file_path = glb_mesh.file.path
        try:
            logging.debug(f"File path: {file_path}")
            if not os.path.exists(file_path):
                logging.error("File does not exist")
                return Response(
                    {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Serve the GLB file as a blob
            response = FileResponse(
                open(file_path, "rb"), content_type="application/octet-stream"
            )
            response["Content-Disposition"] = 'inline; filename="{}"'.format(
                os.path.basename(file_path)
            )
            return response
        except FileNotFoundError:
            logging.error("File not found")
            return Response(
                {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
