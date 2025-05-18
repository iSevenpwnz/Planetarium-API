from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from domes.models import PlanetariumDome
from domes.serializers import PlanetariumDomeSerializer
from show_sessions.models import ShowSession
from show_sessions.serializers import ShowSessionSerializer
from domes.permissions import PlanetariumDomePermissions


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    filterset_fields = ["name", "rows", "seats_in_row"]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "rows", "seats_in_row"]
    ordering = ["id"]

    def get_permissions(self):
        """
        Instantiates and returns the list
        of permissions that this view requires.
        """
        return PlanetariumDomePermissions.get_permissions(self.action)

    @action(detail=True, methods=["get"], url_path="capacity")
    def capacity(self, request, pk=None):
        dome = self.get_object()
        capacity = dome.rows * dome.seats_in_row
        return Response({"capacity": capacity})

    @action(detail=True, methods=["get"], url_path="sessions")
    def sessions(self, request, pk=None):
        dome = self.get_object()
        sessions = ShowSession.objects.filter(planetarium_dome=dome)
        data = ShowSessionSerializer(sessions, many=True).data
        return Response(data)
