from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Trip(models.Model):
    trip_number = models.IntegerField()
    origin = models.CharField(max_length=30, default='Kabayan')
    destination = models.CharField(max_length=30, default='Baguio')
    date = models.DateField()
    time = models.TimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()


 
