from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_number = models.CharField(max_length=10, db_index=True)
    origin = models.CharField(max_length=30, db_index=True)
    destination = models.CharField(max_length=30, db_index=True)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    total_number_of_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.trip_number

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField(default=1)
    date = models.DateField()

    def __str__(self):
        return f"Reservation for {self.user.username} - {self.trip.trip_number} ({self.date})"




