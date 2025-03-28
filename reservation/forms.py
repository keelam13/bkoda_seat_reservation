from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reservation

from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    """
    Form for creating or updating a seat reservation.

    This form allows users to specify the number of seats they want to reserve.
    It includes custom validation to ensure that the number of seats is greater than zero.
    """

    class Meta:
        model = Reservation
        fields = ['number_of_seats']

    def clean_number_of_seats(self):
        """
        Validates the number_of_seats field.

        Ensures that the number of seats is greater than zero.

        Returns:
            int: The cleaned number of seats.

        Raises:
            forms.ValidationError: If the number of seats is less than or equal to zero.
        """
        number_of_seats = self.cleaned_data['number_of_seats']
        if number_of_seats <= 0:
            raise forms.ValidationError("Number of seats must be greater than zero.")
        return number_of_seats