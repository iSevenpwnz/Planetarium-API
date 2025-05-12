from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from shows.models import AstronomyShow, ShowTheme
from shows.serializers import AstronomyShowSerializer, ShowThemeSerializer
from django.db.models import Prefetch


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related(
        Prefetch("themes", queryset=ShowTheme.objects.all())
    )
    serializer_class = AstronomyShowSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filterset_fields = ["themes"]
    search_fields = ["title", "description"]

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-image",
        permission_classes=[permissions.IsAdminUser],
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
