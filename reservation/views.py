from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Trip, User, Reservation
from datetime import datetime
from django.contrib import messages
from .forms import ReservationForm

print("view called")

# Create your views here.
def home_page(request):
    return render(request, 'index.html')


def find_trip(request):
    context = {}
    if request.method == 'POST':
        requested_origin = request.POST.get('origin')
        requested_destination = request.POST.get('destination')
        requested_date_str = request.POST.get('date')

        try:
            # Convert the string date from the form to a datetime.date object
            requested_date = datetime.strptime(requested_date_str, '%Y-%m-%d').date() # Adjust the format string if needed.
            
            trip_list = Trip.objects.filter(
                origin=requested_origin,
                destination=requested_destination,
                date=requested_date
            )
            # Check if there are any results in the QuerySet
            if trip_list.exists():
                for trip in trip_list:
                    print(trip.trip_id)
                return render(request, 'reservation/triplist.html', {'trip_list': trip_list})
            else:
                context["error"] = "Sorry, there are no trips available."
                return render(request, 'index.html', context)

        except ValueError:
            # Handle invalid date format
            context["error"] = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'index.html', context)
    else:
        print(trip_list)
        return render(request, 'index.html')


@login_required
def make_reservation(request, trip_id):
    """View to create a seat reservation."""
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            number_of_seats = form.cleaned_data['number_of_seats']
            reservation_date = form.cleaned_data['date']  # Assuming date field in form.

            # Check if enough seats are available
            if trip.available_seats < number_of_seats:
                messages.error(request, "Not enough seats available.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

            # Check if reservation date matches trip date.
            if reservation_date != trip.date:
                messages.error(request, "Reservation date must match the trip date.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

            # Create the reservation
            reservation = Reservation.objects.create(
                user=request.user,
                trip=trip,
                number_of_seats=number_of_seats,
                date=reservation_date,
            )

            # Update available seats
            trip.available_seats -= number_of_seats
            trip.save()

            messages.success(request, "Reservation successful!")
            return redirect('reservation_list')  # Redirect to reservation list

        else:
            messages.error(request, "Please correct the errors below.")
            print(trip_id)
            return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

    else:
        form = ReservationForm(initial={'date': trip.date}) # pre-fill date with trip date.
        return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

@login_required
def reservation_list(request):
    """View to display the user's reservations."""
    reservations = Reservation.objects.filter(user=request.user).order_by('date')
    return render(request, 'reservation/reservation_list.html', {'reservations': reservations})

        
