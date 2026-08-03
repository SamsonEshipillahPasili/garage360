from django import forms

from django.core.exceptions import PermissionDenied
from accounts.models import UserProfile
from core.models import Booking


class CreateBookingForm(forms.Form):
    car_brand = forms.CharField(max_length=255)
    car_model = forms.CharField(max_length=255)
    car_number_plate = forms.CharField(max_length=255)
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def save(self, client: UserProfile, created_by: UserProfile) -> Booking:
        # Reject cross-organization saving.
        if created_by.organization.id != client.organization.id:
            raise PermissionDenied()

        return Booking.objects.create(
            client=client,
            created_by=created_by,
            **self.cleaned_data
        )
