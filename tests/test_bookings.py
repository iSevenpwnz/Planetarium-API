import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from bookings.models import Reservation


@pytest.mark.django_db
def test_user_sees_only_own_reservations():
    client = APIClient()
    user1 = User.objects.create_user(
        email="user1@test.com", password="pass1234"
    )
    user2 = User.objects.create_user(
        email="user2@test.com", password="pass1234"
    )
    res1 = Reservation.objects.create(user=user1)
    res2 = Reservation.objects.create(user=user2)
    client.force_authenticate(user=user1)
    url = reverse("reservation-list")
    response = client.get(url)
    ids = [r["id"] for r in response.data["results"]]
    assert res1.id in ids
    assert res2.id not in ids


@pytest.mark.django_db
def test_admin_sees_all_reservations():
    client = APIClient()
    admin = User.objects.create_superuser(
        email="admin5@test.com", password="pass1234"
    )
    user = User.objects.create_user(
        email="user3@test.com", password="pass1234"
    )
    res1 = Reservation.objects.create(user=admin)
    res2 = Reservation.objects.create(user=user)
    client.force_authenticate(user=admin)
    url = reverse("reservation-list")
    response = client.get(url)
    ids = [r["id"] for r in response.data["results"]]
    assert res1.id in ids
    assert res2.id in ids
