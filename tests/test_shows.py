import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from shows.models import ShowTheme, AstronomyShow


@pytest.mark.django_db
def test_create_astronomy_show_as_admin():
    client = APIClient()
    admin = User.objects.create_superuser(
        email="admin@test.com", password="pass1234"
    )
    theme = ShowTheme.objects.create(name="Science")
    client.force_authenticate(user=admin)
    url = reverse("astronomyshow-list")
    data = {
        "title": "Test Show",
        "description": "Test desc",
        "themes_ids": [theme.id],
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert AstronomyShow.objects.filter(title="Test Show").exists()
