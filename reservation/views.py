from django.shortcuts import render
from django.views import generic
from .models import Trip


# Create your views here.
class TripListView(generic.ListView):
    queryset = Trip.objects.all()
    template_name = 'reservation/triplist.html'