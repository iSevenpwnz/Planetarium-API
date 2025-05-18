from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from show_sessions.models import ShowSession
from show_sessions.serializers import ShowSessionSerializer, SeatSerializer
from tickets.models import Ticket
from bookings.models import Reservation
from bookings.serializers import ReservationSerializer
from tickets.serializers import TicketSerializer
from django.db import transaction
from django.db.models import Prefetch
from rest_framework.exceptions import ValidationError
from show_sessions.permissions import ShowSessionPermissions


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related(
        "astronomy_show", "planetarium_dome"
    ).prefetch_related(
        Prefetch(
            "tickets", queryset=Ticket.objects.select_related("reservation")
        )
    )
    serializer_class = ShowSessionSerializer
    filterset_fields = ["astronomy_show", "planetarium_dome", "show_time"]
    ordering_fields = ["id", "show_time", "astronomy_show", "planetarium_dome"]
    ordering = ["show_time", "id"]

    def get_permissions(self):
        return ShowSessionPermissions.get_permissions(self.action)

    @action(detail=True, methods=["get"], url_path="available-seats")
    def available_seats(self, request, pk=None):
        session = self.get_object()
        dome = session.planetarium_dome
        taken = Ticket.objects.filter(show_session=session).values_list(
            "row", "seat"
        )
        all_seats = [
            {"row": row, "seat": seat}
            for row in range(1, dome.rows + 1)
            for seat in range(1, dome.seats_in_row + 1)
        ]
        available = [
            s for s in all_seats if (s["row"], s["seat"]) not in taken
        ]
        return Response({"available_seats": available})

    @action(
        detail=True,
        methods=["post"],
        url_path="book",
    )
    @transaction.atomic
    def book(self, request, pk=None):
        """Books one or more seats for this session for the current user."""
        show_session = self.get_object()
        dome = show_session.planetarium_dome
        user = request.user
        seats_data = request.data

        if not isinstance(seats_data, list):
            raise ValidationError("List of seats was expected.")

        seat_serializer = SeatSerializer(data=seats_data, many=True)
        seat_serializer.is_valid(raise_exception=True)
        validated_seats = seat_serializer.validated_data

        if not validated_seats:
            raise ValidationError("List of seats cannot be empty.")

        taken_seats_qs = Ticket.objects.filter(show_session=show_session)
        existing_tickets = set(taken_seats_qs.values_list("row", "seat"))

        seats_to_book = []
        for seat_data in validated_seats:
            row = seat_data["row"]
            seat = seat_data["seat"]

            if not (1 <= row <= dome.rows and 1 <= seat <= dome.seats_in_row):
                raise ValidationError(
                    f"Seat (row {row}, seat {seat}) does not exist in dome "
                    f'"{dome.name}".'
                )

            if (row, seat) in existing_tickets:
                raise ValidationError(
                    f"Seat (row {row}, seat {seat}) is already booked "
                    f"for this session."
                )

            if (row, seat) in [(s["row"], s["seat"]) for s in seats_to_book]:
                raise ValidationError(
                    f"Seat (row {row}, seat {seat}) is mentioned multiple times "
                    f"in the request."
                )

            seats_to_book.append(seat_data)

        reservation = Reservation.objects.create(user=user)

        created_tickets = []
        for seat_data in seats_to_book:
            ticket = Ticket.objects.create(
                row=seat_data["row"],
                seat=seat_data["seat"],
                show_session=show_session,
                reservation=reservation,
            )
            created_tickets.append(ticket)

        reservation_serializer = ReservationSerializer(reservation)
        ticket_serializer = TicketSerializer(created_tickets, many=True)

        return Response(
            {
                "reservation": reservation_serializer.data,
                "tickets": ticket_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
