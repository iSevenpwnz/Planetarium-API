from rest_framework import viewsets, permissions
from bookings.models import Reservation
from bookings.serializers import ReservationSerializer
from bookings.permissions import IsOwnerOrAdmin


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filterset_fields = ["user", "created_at"]
    ordering_fields = ["created_at", "user"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        qs = Reservation.objects.select_related("user")
        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
