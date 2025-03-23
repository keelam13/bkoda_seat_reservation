from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['number_of_seats', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_number_of_seats(self):
        number_of_seats = self.cleaned_data['number_of_seats']
        if number_of_seats <= 0:
            raise forms.ValidationError("Number of seats must be greater than zero.")
        return number_of_seats

    def clean_date(self):
        date = self.cleaned_data['date']
        return date

