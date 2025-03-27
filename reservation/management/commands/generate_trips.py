from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, time
from random import choice
from reservation.models import Trip

class Command(BaseCommand):
    help = 'Generates sample trips'

    def handle(self, *args, **options):
        latest_trip = Trip.objects.order_by('-date').first()
        start_date = latest_trip.date
        end_date = start_date + timedelta(days=14)  # Generate for the next 14 days
        time_intervals = [time(hour) for hour in range(6, 16, 2)]

        while start_date <= end_date:
            used_times_kb = set()  # Track used times for Kabayan-Baguio
            used_times_bk = set()  # Track used times for Baguio-Kabayan

            #Kabayan to Baguio
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

            #Baguio to Kabayan
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
        """Gets a unique time, preventing duplicates."""
        available_times = [t for t in time_intervals if t not in used_times]
        if not available_times:
            raise ValueError("All time intervals have been used for this date.")
        return choice(available_times)