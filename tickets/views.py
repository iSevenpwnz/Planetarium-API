from rest_framework import viewsets, permissions
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from tickets.permissions import IsOwnerOrAdmin


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("show_session", "reservation")
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filterset_fields = ["show_session", "reservation", "row", "seat"]
    ordering_fields = ["id", "show_session", "reservation", "row", "seat"]
    ordering = ["id"]

    def get_queryset(self):
        user = self.request.user
        qs = Ticket.objects.select_related("show_session", "reservation")
        if user.is_staff:
            return qs
        return qs.filter(reservation__user=user)
