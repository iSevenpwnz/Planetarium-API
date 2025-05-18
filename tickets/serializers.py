from rest_framework import serializers
from tickets.models import Ticket
from show_sessions.models import ShowSession
from bookings.models import Reservation


class TicketSerializer(serializers.ModelSerializer):
    show_session = serializers.StringRelatedField(read_only=True)
    show_session_id = serializers.PrimaryKeyRelatedField(
        queryset=ShowSession.objects.all(),
        source="show_session",
        write_only=True,
    )
    reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all()
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "show_session",
            "show_session_id",
            "reservation",
        ]

    def validate(self, data):
        show_session = data.get("show_session")
        row = data.get("row")
        seat = data.get("seat")
        if Ticket.objects.filter(
            show_session=show_session, row=row, seat=seat
        ).exists():
            raise serializers.ValidationError(
                "This seat is already taken for this session."
            )
        return data
