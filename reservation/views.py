from django.shortcuts import render
from django.views import generic
from .models import Trip
from datetime import datetime


# Create your views here.
def home_page(request):
    return render(request, 'reservation/index.html')


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
                return render(request, 'reservation/triplist.html', {'trip_list': trip_list})
            else:
                context["error"] = "Sorry, there are no trips available."
                return render(request, 'reservation/index.html', context)

        except ValueError:
            # Handle invalid date format
            context["error"] = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'reservation/index.html', context)
    else:
        return render(request, 'reservation/index.html')
