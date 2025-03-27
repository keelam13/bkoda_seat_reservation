from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dal import autocomplete
from datetime import datetime, timedelta
from .models import Trip, User, Reservation
from .forms import ReservationForm

print("view called")

# Create your views here.
def home_page(request):
    return render(request, 'index.html')


def find_trip(request):
    context = {}
    requested_origin = request.GET.get('origin')
    requested_destination = request.GET.get('destination')
    requested_date_str = request.GET.get('date')
    today = datetime.now().date()
    now = datetime.now()

    if requested_date_str and requested_origin and requested_destination:
        try:
            requested_date = datetime.strptime(requested_date_str, '%Y-%m-%d').date()
            previous_day = requested_date - timedelta(days=1)
            next_day = requested_date + timedelta(days=1)

            trip_list = Trip.objects.filter(
                origin__icontains=requested_origin,
                destination__icontains=requested_destination,
                date=requested_date
            )

            # Filter out past trips
            trip_list = [trip for trip in trip_list if datetime.combine(trip.date, trip.time) >= now]

            trip_list = sorted(trip_list, key=lambda trip: trip.time)

            if len(trip_list) > 0:
                context = {
                    'trip_list': trip_list,
                    'origin': requested_origin,
                    'destination': requested_destination,
                    'current_day': requested_date,
                    'previous_day': previous_day,
                    'next_day': next_day,
                }
                for trip in trip_list:
                    print(f"Trip: {trip.date} {trip.time}")
                return render(request, 'reservation/triplist.html', context)
            elif requested_date < today:
                context["error"] = "Sorry, the date you requested is in the past."
                # context["previous_day"] = previous_day
                # context["next_day"] = next_day
                # context["current_day"] = requested_date

                # return render(request, 'reservation/triplist.html', context)
            else:
                context["error"] = "Sorry, there are no trips available yet."
        except ValueError:
            context["error"] = "Invalid date format. Please use YYYY-MM-DD."
    
    origins = Trip.objects.values_list('origin', flat=True).distinct()
    destinations = Trip.objects.values_list('destination', flat=True).distinct()
    context['origins'] = origins
    context['destinations'] = destinations
    return render(request, 'index.html', context)

class OriginAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Trip.objects.values_list('origin', flat=True).distinct()

        if self.q:
            qs = qs.filter(origin__icontains=self.q)
        return qs

class DestinationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Trip.objects.values_list('destination', flat=True).distinct()

        if self.q:
            qs = qs.filter(destination__icontains=self.q)
        return qs


@login_required
def make_reservation(request, trip_id):
    """View to create a seat reservation."""
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            number_of_seats = form.cleaned_data['number_of_seats']

            # Check if enough seats are available
            if trip.available_seats < number_of_seats:
                messages.error(request, "Not enough seats available.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

            # Create the reservation
            print(f"Trip time before assignment: {trip.time}")
            reservation = Reservation.objects.create(
                user=request.user,
                trip=trip,
                number_of_seats=number_of_seats,
                date=trip.date,
                time=trip.time,
            )
            print(f"Reservation time: {reservation.time}") 
            # Update available seats
            trip.available_seats -= number_of_seats
            trip.save()

            messages.success(request, "Reservation successful!")
            return redirect('reservation_list')  # Redirect to reservation list

        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})
    else:
        form = ReservationForm(initial={'date': trip.date}) # pre-fill date with trip date.
        return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})


@login_required
def reservation_list(request):
    """View to display the user's reservations."""
    reservations = Reservation.objects.filter(user=request.user).order_by('date')
    return render(request, 'reservation/reservation_list.html', {'reservations': reservations})


@login_required
def edit_reservation(request, reservation_id):
    """View to edit a reservation."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    trip = reservation.trip
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        reserved_seats = reservation.number_of_seats
        print(f'reserved seats - {reserved_seats}')

        if form.is_valid():
            number_of_seats = form.cleaned_data['number_of_seats']

            # Calculate the difference in seats
            seat_diff = number_of_seats - reserved_seats
            print(f'seat-diff {seat_diff}, no_of_seats {number_of_seats}, reserved_seats {reserved_seats}')

            # Check if enough seats are available
            if trip.available_seats < seat_diff:
                messages.error(request, "Not enough seats available.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

            # Update available seats
            trip.available_seats -= seat_diff

            print(f'av_seats_left - {trip.available_seats}')
            trip.save()

            # Save the reservation
            form.save()
            messages.success(request, "Reservation updated successfully!")
            return redirect('reservation_list')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})


@login_required
def cancel_reservation(request, reservation_id):
    """View to cancel a reservation."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    trip = reservation.trip

    if request.method == 'POST':
        # Return the seats to available seats on the trip
        trip.available_seats += reservation.number_of_seats
        trip.save()

        reservation.delete()
        messages.success(request, "Reservation canceled successfully!")
        return redirect('reservation_list')

    return render(request, 'reservation/cancel_confirmation.html', {'reservation': reservation})