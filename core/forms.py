from django import forms

from django.core.exceptions import PermissionDenied
from accounts.models import UserProfile
from core.models import Booking, Quotation, QuotationLine


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

        return Booking.objects.create_booking(
            client=client,
            created_by=created_by,
            data=self.cleaned_data
        )

class CreateQuotationLineForm(forms.Form):
    description = forms.CharField(max_length=255)
    quantity = forms.IntegerField()
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than 0')
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data['unit_price']
        if unit_price <= 0:
            raise forms.ValidationError('Unit price must be greater than 0')
        return unit_price

    def save(self, quotation: Quotation) -> QuotationLine:
        return QuotationLine.objects.create(
            quotation=quotation,
            **self.cleaned_data
        )
