from rest_framework import serializers
from shows.models import AstronomyShow, ShowTheme


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ["id", "name"]


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)
    themes_ids = serializers.PrimaryKeyRelatedField(
        queryset=ShowTheme.objects.all(),
        many=True,
        write_only=True,
        source="themes",
    )

    class Meta:
        model = AstronomyShow
        fields = [
            "id",
            "title",
            "description",
            "image",
            "themes",
            "themes_ids",
        ]
