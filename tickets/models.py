from django.db import models
from show_sessions.models import ShowSession
from bookings.models import Reservation


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self):
        return (
            f"Ticket: Row {self.row}, Seat {self.seat} for {self.show_session}"
        )
