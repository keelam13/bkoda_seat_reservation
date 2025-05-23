from django.contrib import admin
from .models import Trip, Reservation
from django.db.models import Sum


class ReservationInline(admin.TabularInline):
    """
    Inline admin interface for Reservation objects within the Trip admin.

    Allows editing of Reservation objects directly within the Trip admin page.
    """
    model = Reservation
    extra = 0


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Admin interface for the Trip model.

    Provides list display, filtering, search functionality, and inline
    editing for Trip objects.
    Also calculates and displays the total number of seats reserved
    for each trip.
    """
    list_display = (
        'trip_number',
        'origin',
        'destination',
        'date',
        'time',
        'total_seats',
        'available_seats',
        'total_seats_reserved')
    list_filter = ('origin', 'destination', 'date')
    search_fields = ('trip_number', 'origin', 'destination')
    inlines = [ReservationInline]
    ordering = ('-date', '-time')

    def total_seats_reserved(self, obj):
        """
        Calculates the total number of seats reserved for a given trip.

        Args:
            obj (Trip): The Trip object for which to calculate reserved seats.

        Returns:
            int: The total number of seats reserved, or 0 if no reservations
            exist.
        """
        total_reserved = Reservation.objects.filter(trip=obj).aggregate(
            total_reserved=Sum('number_of_seats'))['total_reserved'] or 0
        return total_reserved

    total_seats_reserved.short_description = 'Total Seats Reserved'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin interface for the Reservation model.
    Provides list display, filtering, search functionality, and read-only
    user field.
    """
    list_display = ('id', 'user', 'trip', 'date', 'time', 'number_of_seats')
    list_filter = ('user', 'trip', 'date')
    search_fields = (
        'user__username',
        'trip__trip_number',
        'trip__origin',
        'id',
        'date'
    )
    ordering = ('-date', '-time')
    readonly_fields = ('user',)  # User can't be changed from the admin panel.
    fieldsets = (
        ('Reservation Details', {
            'fields': ('user', 'trip', 'date', 'time', 'number_of_seats')
        }),
    )
