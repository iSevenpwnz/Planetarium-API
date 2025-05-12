from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from show_sessions.models import ShowSession
from show_sessions.serializers import ShowSessionSerializer
from tickets.models import Ticket
from django.db.models import Prefetch


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related(
        "astronomy_show", "planetarium_dome"
    ).prefetch_related(
        Prefetch(
            "tickets", queryset=Ticket.objects.select_related("reservation")
        )
    )
    serializer_class = ShowSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["astronomy_show", "planetarium_dome", "show_time"]

    @action(detail=True, methods=["get"], url_path="available-seats")
    def available_seats(self):
        session = self.get_object()
        dome = session.planetarium_dome
        taken = Ticket.objects.filter(show_session=session).values_list(
            "row", "seat"
        )
        all_seats = [
            {"row": row, "seat": seat}
            for row in range(1, dome.rows + 1)
            for seat in range(1, dome.seats_in_row + 1)
        ]
        available = [
            s for s in all_seats if (s["row"], s["seat"]) not in taken
        ]
        return Response({"available_seats": available})
