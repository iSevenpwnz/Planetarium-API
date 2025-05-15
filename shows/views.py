from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from shows.models import AstronomyShow, ShowTheme
from shows.serializers import AstronomyShowSerializer, ShowThemeSerializer
from django.db.models import Prefetch


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    ordering_fields = ["name", "id"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related(
        Prefetch("themes", queryset=ShowTheme.objects.all())
    )
    serializer_class = AstronomyShowSerializer
    filterset_fields = ["themes"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "id"]
    ordering = ["title"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action == "upload_image":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        show = self.get_object()
        image = request.FILES.get("image")
        if not image:
            return Response(
                {"detail": "No image provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        show.image = image
        show.save()
        return Response(self.get_serializer(show).data)
