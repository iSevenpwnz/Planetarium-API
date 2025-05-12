import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from bookings.models import Reservation
from show_sessions.models import ShowSession
from tickets.models import Ticket
from shows.models import AstronomyShow, ShowTheme
from domes.models import PlanetariumDome


@pytest.mark.django_db
def test_cannot_create_ticket_for_taken_seat():
    client = APIClient()
    admin = User.objects.create_superuser(
        email="admin4@test.com", password="pass1234"
    )
    user = User.objects.create_user(email="user@test.com", password="pass1234")
    theme = ShowTheme.objects.create(name="Physics")
    show = AstronomyShow.objects.create(title="Show2", description="desc")
    show.themes.add(theme)
    dome = PlanetariumDome.objects.create(name="Dome2", rows=3, seats_in_row=3)
    session = ShowSession.objects.create(
        astronomy_show=show,
        planetarium_dome=dome,
        show_time="2030-01-01T12:00:00Z",
    )
    reservation = Reservation.objects.create(user=user)

    Ticket.objects.create(
        row=1, seat=1, show_session=session, reservation=reservation
    )
    client.force_authenticate(user=admin)
    url = reverse("ticket-list")
    data = {
        "row": 1,
        "seat": 1,
        "show_session_id": session.id,
        "reservation_id": reservation.id,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 400
    assert "місце вже зайняте" in str(response.data).lower()
