from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="shows/images/", blank=True, null=True)
    themes = models.ManyToManyField(ShowTheme, related_name="shows")

    def __str__(self):
        return self.title
