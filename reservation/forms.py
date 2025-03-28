from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reservation, Trip

class ReservationForm(forms.ModelForm):
    """
    Form for creating or updating a seat reservation.

    This form allows users to specify the number of seats they want to reserve.
    It includes custom validation to ensure that the number of seats is greater than zero
    and less than or equal to the total available seats for the trip.
    """

    class Meta:
        model = Reservation
        fields = ['number_of_seats']

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)  # Get the trip instance from kwargs
        super().__init__(*args, **kwargs)

    def clean_number_of_seats(self):
        """
        Validates the number_of_seats field.

        Ensures that the number of seats is greater than zero and does not exceed the
        trip's total seats, considering existing reservations.

        Returns:
            int: The cleaned number of seats.

        Raises:
            forms.ValidationError: If the number of seats is less than or equal to zero,
                or if the new total reserved seats exceed the trip's total seats.
        """
        number_of_seats = self.cleaned_data['number_of_seats']

        if number_of_seats <= 0:
            raise forms.ValidationError("Number of seats must be greater than zero.")

        if self.trip:
            if self.instance.pk:  # Updating existing reservation
                original_seats = Reservation.objects.get(pk=self.instance.pk).number_of_seats
                other_reservations = Reservation.objects.filter(trip=self.trip).exclude(pk=self.instance.pk)
                total_other_seats = sum(r.number_of_seats for r in other_reservations)
                new_total_seats = number_of_seats + total_other_seats

                if new_total_seats > self.trip.total_seats:
                    raise forms.ValidationError(
                        f"The total reserved seats ({new_total_seats}) cannot exceed the trip's total seats ({self.trip.total_seats})."
                    )
            else:  # New reservation
                other_reservations = Reservation.objects.filter(trip=self.trip)
                total_other_seats = sum(r.number_of_seats for r in other_reservations)
                new_total_seats = number_of_seats + total_other_seats

                if new_total_seats > self.trip.total_seats:
                    raise forms.ValidationError(
                        f"The total reserved seats ({new_total_seats}) cannot exceed the trip's total seats ({self.trip.total_seats})."
                    )

        return number_of_seats