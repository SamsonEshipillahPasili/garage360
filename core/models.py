from django.db import models
from django.utils import timezone

from accounts.models import UserProfile
from utils.models import TimestampedModel

class Booking(TimestampedModel):
    # the client for the booking
    client = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # The car to be booked in the garage.
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_yom = models.CharField(max_length=255)
    car_number_plate = models.CharField(max_length=255)

    # booking metadata
    booking_date = models.DateField(default=timezone.now)
    booked_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='staff_bookings'
    )
