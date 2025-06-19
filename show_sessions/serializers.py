from rest_framework import serializers
from show_sessions.models import ShowSession
from shows.models import AstronomyShow
from domes.models import PlanetariumDome


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.StringRelatedField(read_only=True)
    astronomy_show_id = serializers.PrimaryKeyRelatedField(
        queryset=AstronomyShow.objects.all(),
        source="astronomy_show",
        write_only=True,
    )
    planetarium_dome = serializers.StringRelatedField(read_only=True)
    planetarium_dome_id = serializers.PrimaryKeyRelatedField(
        queryset=PlanetariumDome.objects.all(),
        source="planetarium_dome",
        write_only=True,
    )

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "astronomy_show_id",
            "planetarium_dome",
            "planetarium_dome_id",
            "show_time",
        ]


class SeatSerializer(serializers.Serializer):
    row = serializers.IntegerField(min_value=1)
    seat = serializers.IntegerField(min_value=1)

    class Meta:
        fields = ["row", "seat"]
