from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    trip_number = models.CharField(max_length=10)
    origin = models.CharField(max_length=30, blank=True, db_index=True)
    destination = models.CharField(max_length=30, blank=True, db_index=True)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    total_number_of_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.trip_number
    

