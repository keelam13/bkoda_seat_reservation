from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, time
from random import choice
from reservation.models import Trip

class Command(BaseCommand):
    """
    Generates sample trips for the next 14 days, starting from the latest trip date.

    This command creates 5 trips per day for both "Kabayan-Baguio" and "Baguio-Kabayan" routes,
    using predefined time intervals and ensuring unique trip times for each route per day.
    """

    help = 'Generates sample trips'

    def handle(self, *args, **options):
        """
        Handles the generation of sample trips.

        Retrieves the latest trip date, calculates the end date (14 days from the start date),
        and generates trips for each day within the range.
        """

        latest_trip = Trip.objects.order_by('-date').first()

        if latest_trip:
            start_date = latest_trip.date + timedelta(days=1)
        else:
            # Handle the case where there are no trips
            from datetime import date
            start_date = date.today()

        start_date = latest_trip.date
        end_date = start_date + timedelta(days=1)  # Generate for the next day
        time_intervals = [time(hour) for hour in range(6, 16, 2)]

        current_date = start_date

        while current_date <= end_date:
            used_times_kb = set()  # Track used times for Kabayan-Baguio
            used_times_bk = set()  # Track used times for Baguio-Kabayan

            # Kabayan to Baguio
            for _ in range(5):  # Generate 5 trips per day
                trip_time = self.get_unique_time(time_intervals, used_times_kb)
                used_times_kb.add(trip_time)
                total_number_of_seats = 12
                available_seats = total_number_of_seats

                Trip.objects.create(
                    origin="Kabayan",
                    destination="Baguio City",
                    date=current_date,
                    time=trip_time,
                    total_seats=total_number_of_seats,
                    available_seats=available_seats,
                    trip_number=f'KAB-BAG{current_date.strftime("%Y%m%d")}-{trip_time.strftime("%H%M")}'
                )

            # Baguio to Kabayan
            for _ in range(5):  # Generate 5 trips per day
                trip_time = self.get_unique_time(time_intervals, used_times_bk)
                used_times_bk.add(trip_time)
                total_number_of_seats = 12
                available_seats = total_number_of_seats

                Trip.objects.create(
                    origin="Baguio",
                    destination="Kabayan",
                    date=current_date,
                    time=trip_time,
                    total_seats=total_number_of_seats,
                    available_seats=available_seats,
                    trip_number=f'BAG-KAB-{current_date.strftime("%Y%m%d")}-{trip_time.strftime("%H%M")}'
                )

            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Trips generated successfully'))

    def get_unique_time(self, time_intervals, used_times):
        """
        Gets a unique time from the available time intervals.

        Ensures that the selected time has not been used for the current route and date.

        Args:
            time_intervals (list): A list of time objects representing available trip times.
            used_times (set): A set of time objects that have already been used.

        Returns:
            time: A unique time object.

        Raises:
            ValueError: If all time intervals have been used for the current date.
        """
        available_times = [t for t in time_intervals if t not in used_times]
        if not available_times:
            raise ValueError("All time intervals have been used for this date.")
        return choice(available_times)