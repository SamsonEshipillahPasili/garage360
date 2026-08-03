from django.db import models
from django.utils import timezone

from accounts.models import UserProfile
from utils.models import TimestampedModel

class Booking(TimestampedModel):
    class BookingStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    # the client for the booking
    client = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # the status of the booking
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )

    # The car to be booked in the garage.
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_yom = models.CharField(max_length=255)
    car_number_plate = models.CharField(max_length=255)

    # booking metadata
    booking_date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='staff_bookings'
    )


class Quotation(TimestampedModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='quotation')
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField()

class QuotationLine(TimestampedModel):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='quotation_lines')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.PositiveIntegerField()

