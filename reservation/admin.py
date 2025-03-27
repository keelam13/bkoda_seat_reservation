from django.contrib import admin
from .models import Trip, Reservation
from django.db.models import Sum

# Register your models here.
class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_number', 'origin', 'destination', 'date', 'time', 'total_seats', 'available_seats', 'total_seats_reserved')
    list_filter = ('origin', 'destination', 'date')
    search_fields = ('trip_number', 'origin', 'destination')
    inlines = [ReservationInline]
    ordering = ('-date', '-time')

    def total_seats_reserved(self, obj):
        """Calculates the total seats reserved for a trip."""
        total_reserved = Reservation.objects.filter(trip=obj).aggregate(total_reserved=Sum('number_of_seats'))['total_reserved'] or 0
        return total_reserved

    total_seats_reserved.short_description = 'Total Seats Reserved'


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