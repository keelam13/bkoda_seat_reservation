from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Trip(models.Model):
    """
    Represents a trip with details like origin, destination, date, time,
    and seat availability.
    """
    trip_id = models.AutoField(primary_key=True)
    trip_number = models.CharField(max_length=30, db_index=True)
    origin = models.CharField(max_length=30, db_index=True)
    destination = models.CharField(max_length=30, db_index=True)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def update_available_seats(self, number_of_seats, operation='subtract'):
        """
        Updates the available seats for the trip.

        Args:
            number_of_seats (int): The number of seats to add or subtract.
            operation (str): 'subtract' to decrease seats, 'add' to increase
            seats. Defaults to 'subtract'.
        """
        if operation == 'subtract':
            self.available_seats -= number_of_seats
        elif operation == 'add':
            self.available_seats += number_of_seats
        self.save()

    def __str__(self):
        """
        Returns a string representation of the trip.
        """
        return (
            f"{self.trip_number}: {self.origin} to {self.destination}"
            f"({self.date} {self.time})"
        )


class Reservation(models.Model):
    """
    Represents a reservation made by a user for a trip.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField(default=1)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update trip's available seats.
        """
        # Check if the reservation is being created or updated
        if self.pk:  # Updating existing reservation
            original_seats = Reservation.objects.get(
                pk=self.pk).number_of_seats
            seat_diff = self.number_of_seats - original_seats
            if seat_diff != 0:
                self.trip.update_available_seats(
                    abs(seat_diff), 'subtract' if seat_diff > 0 else 'add')
        else:  # Creating new reservation
            self.trip.update_available_seats(self.number_of_seats, 'subtract')

        super().save(*args, **kwargs)
