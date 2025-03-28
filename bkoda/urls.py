from django.contrib import admin
from django.urls import path, include
from reservation import views

"""
URL configuration for the reservation app.

This module defines the URL patterns for the reservation application.
It includes URLs for:
- Admin interface
- User authentication (allauth)
- Home page
- Trip search and display
- Autocomplete for origin and destination
- Reservation creation, listing, editing, and cancellation.
"""

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Allauth URLs for user authentication
    path('accounts/', include('allauth.urls')),

    # Home page URL
    path('', views.home_page, name='home'),

    # Find trip search URL
    path('find_trip', views.find_trip, name="find_trip"),

    # Autocomplete URLs for origin and destination fields
    path(
        'origin-autocomplete/',
        views.OriginAutocomplete.as_view(),
        name='origin-autocomplete',
    ),
    path(
        'destination-autocomplete/',
        views.DestinationAutocomplete.as_view(),
        name='destination-autocomplete',
    ),

    # Reservation creation URL
    path('create/<int:trip_id>', views.make_reservation, name="make_reservation"),

    # User reservation list URL
    path('reservation_list/', views.reservation_list, name="reservation_list"),

    # Reservation editing URL
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),

    # Reservation cancellation URL
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]