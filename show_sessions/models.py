from django.db import models
from shows.models import AstronomyShow
from domes.models import PlanetariumDome


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE, related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE, related_name="sessions"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.astronomy_show.title} @ "
            f"{self.planetarium_dome.name} ({self.show_time})"
        )
