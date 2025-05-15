import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from shows.models import AstronomyShow, ShowTheme
from domes.models import PlanetariumDome
from show_sessions.models import ShowSession


@pytest.mark.django_db
def test_create_show_session_as_admin():
    client = APIClient()
    admin = User.objects.create_superuser(
        email="admin3@test.com", password="pass1234"
    )
    theme = ShowTheme.objects.create(name="Space")
    show = AstronomyShow.objects.create(title="Show1", description="desc")
    show.themes.add(theme)
    dome = PlanetariumDome.objects.create(name="Dome1", rows=5, seats_in_row=5)
    client.force_authenticate(user=admin)
    url = reverse("showsession-list")
    data = {
        "astronomy_show_id": show.id,
        "planetarium_dome_id": dome.id,
        "show_time": "2030-01-01T12:00:00Z",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert ShowSession.objects.filter(
        astronomy_show=show, planetarium_dome=dome
    ).exists()
