from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from shows.models import AstronomyShow, ShowTheme
from shows.serializers import AstronomyShowSerializer, ShowThemeSerializer
from django.db.models import Prefetch
from shows.permissions import ShowThemePermissions, AstronomyShowPermissions


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    ordering_fields = ["name", "id"]
    ordering = ["name"]

    def get_permissions(self):
        return ShowThemePermissions.get_permissions(self.action)


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
        return AstronomyShowPermissions.get_permissions(self.action)

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
