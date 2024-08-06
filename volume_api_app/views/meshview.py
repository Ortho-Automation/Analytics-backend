from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import FileResponse
import logging
import os


class BaseMeshViewSet(viewsets.ModelViewSet):
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
    def upload_mesh(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mesh_file = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="content")
    def content(self, request, pk=None):
        mesh = self.get_object()
        file_path = mesh.file.path
        try:
            logging.debug(f"File path: {file_path}")
            if not os.path.exists(file_path):
                logging.error("File does not exist")
                return Response(
                    {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response = FileResponse(
                open(file_path, "rb"), content_type=self.get_content_type()
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

    @action(detail=True, methods=["get"], url_path="get_json")
    def get_json(self, request, pk=None):
        mesh = self.get_object()
        if not mesh.data:
            return Response(
                {"error": "No JSON data available"}, status=status.HTTP_404_NOT_FOUND
            )

        file_path = mesh.data.path
        try:
            logging.debug(f"File path: {file_path}")
            if not os.path.exists(file_path):
                logging.error("File does not exist")
                return Response(
                    {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response = FileResponse(
                open(file_path, "rb"), content_type="application/json"
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

    def get_content_type(self):
        raise NotImplementedError("You must define get_content_type in subclasses")
