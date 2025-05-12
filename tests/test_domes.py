from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from domes.models import PlanetariumDome

# Create your tests here.


@pytest.mark.django_db
def test_create_dome_as_admin():
    client = APIClient()
    admin = User.objects.create_superuser(
        email="admin2@test.com", password="pass1234"
    )
    client.force_authenticate(user=admin)
    url = reverse("planetariumdome-list")
    data = {"name": "Main Dome", "rows": 10, "seats_in_row": 20}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert PlanetariumDome.objects.filter(name="Main Dome").exists()
