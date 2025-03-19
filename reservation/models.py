from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_number = models.CharField(max_length=30, db_index=True)
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
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Reservation for {self.user.username} - {self.trip.trip_number} ({self.date})"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip', 'date', 'time', 'number_of_seats')
    list_filter = ('user', 'trip', 'date')
    search_fields = ('user__username', 'trip__trip_number', 'trip__origin','id', 'date')
    ordering = ('-date', '-time')
    readonly_fields = ('user',) #user can not be changed from the admin panel.
    fieldsets = (
        ('Reservation Details', {
            'fields': ('user', 'trip', 'date', 'time', 'number_of_seats')
        }),
    )