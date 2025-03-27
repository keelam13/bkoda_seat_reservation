from django.contrib import admin
from .models import Trip, Reservation

# Register your models here.
class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_number', 'origin', 'destination', 'date', 'time', 'total_seats', 'available_seats', 'reservation_count')
    search_fields = ('trip_number', 'origin', 'date')
    list_filter = ('origin', 'destination', 'date')
    inlines = [ReservationInline]
    ordering = ('date', 'time')

    def reservation_count(self, obj):
        return obj.reservation_set.count()
    reservation_count.short_description = 'Reservations'


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