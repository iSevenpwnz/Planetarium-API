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
    reservation = serializers.StringRelatedField(read_only=True)
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        source="reservation",
        write_only=True,
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
            "reservation_id",
        ]

    def validate(self, data):
        show_session = data.get("show_session")
        row = data.get("row")
        seat = data.get("seat")
        if Ticket.objects.filter(
            show_session=show_session, row=row, seat=seat
        ).exists():
            raise serializers.ValidationError(
                "Це місце вже зайняте для цієї сесії."
            )
        return data
