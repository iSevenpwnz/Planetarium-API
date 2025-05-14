from django.db import models
from django.contrib.auth import get_user_model


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reservations"
    )

    def __str__(self):
        return (
            f"Reservation {self.id} by {self.user.email} at {self.created_at}"
        )
