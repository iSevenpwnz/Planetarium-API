from rest_framework import serializers
from bookings.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]
        read_only_fields = ["created_at", "user"]
