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
            ).order_by('time')

             # Filter out trips in the past hours
            if requested_date == today:
                trip_list = trip_list.filter(time__gte=now.time())

            trip_list = trip_list.order_by('time')

            if trip_list.exists():
                context = {
                    'trip_list': trip_list,
                    'origin': requested_origin,
                    'destination': requested_destination,
                    'current_day': requested_date,
                    'previous_day': previous_day,
                    'next_day': next_day,
                }
                return render(request, 'reservation/triplist.html', context)
            elif requested_date < today:
                context["error"] = "Sorry, the date you requested is in the past."
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
            return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

    else:
        form = ReservationForm(initial={'date': trip.date}) # pre-fill date with trip date.
        return render(request, 'reservation/reservation_form.html', {'form': form, 'trip': trip})

@login_required
def reservation_list(request):
    """View to display the user's reservations."""
    reservations = Reservation.objects.filter(user=request.user).order_by('date')
    return render(request, 'reservation/reservation_list.html', {'reservations': reservations})

        
