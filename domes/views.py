from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from domes.models import PlanetariumDome
from domes.serializers import PlanetariumDomeSerializer
from show_sessions.models import ShowSession
from show_sessions.serializers import ShowSessionSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["name", "rows", "seats_in_row"]
    search_fields = ["name"]

    @action(detail=True, methods=["get"], url_path="capacity")
    def capacity(self):
        dome = self.get_object()
        capacity = dome.rows * dome.seats_in_row
        return Response({"capacity": capacity})

    @action(detail=True, methods=["get"], url_path="sessions")
    def sessions(self):
        dome = self.get_object()
        sessions = ShowSession.objects.filter(planetarium_dome=dome)
        data = ShowSessionSerializer(sessions, many=True).data
        return Response(data)
