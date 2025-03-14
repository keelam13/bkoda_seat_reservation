from django.shortcuts import render, redirect
from .models import Trip, User
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm



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


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Instantiate the form with POST data
        if form.is_valid():
            user = form.save(commit=False)  # Create a new user object but don't save it yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Now save the user
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            # Form is invalid; render the registration page with the form and errors
            return render(request, 'reservation/registration.html', {'form': form})
    else:
        form = RegistrationForm()  # Create an empty form for GET requests
        return render(request, 'reservation/registration.html', {'form': form})
    

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log in the user
                messages.success(request, 'You are logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'reservation/login.html', {'form': form})
        else:
            return render(request, 'reservation/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'reservation/login.html', {'form': form})


def signout(request):
    logout(request)  # Log the user out
    messages.success(request, 'You are logged out!')
    return redirect('home')  # Redirect to the home page or another appropriate page