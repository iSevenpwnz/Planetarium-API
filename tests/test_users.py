import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse("user-register")
    data = {
        "email": "newuser@test.com",
        "password": "pass1234",
        "first_name": "Test",
        "last_name": "User",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert User.objects.filter(email="newuser@test.com").exists()


@pytest.mark.django_db
def test_user_me_endpoint():
    client = APIClient()
    user = User.objects.create_user(
        email="me@test.com", password="pass1234", first_name="Me"
    )
    client.force_authenticate(user=user)
    url = reverse("user-me")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["email"] == "me@test.com"
    assert response.data["first_name"] == "Me"


@pytest.mark.django_db
def test_user_list_permissions():
    client = APIClient()
    user = User.objects.create_user(
        email="userlist@test.com", password="pass1234"
    )
    admin = User.objects.create_superuser(
        email="adminlist@test.com", password="pass1234"
    )
    client.force_authenticate(user=user)
    url = reverse("user-list")
    response = client.get(url)
    assert response.status_code == 403

    # Test admin can list users (optional, but good practice)
    client.force_authenticate(user=admin)
    response = client.get(url)
    assert len(response.data["results"]) >= 2
