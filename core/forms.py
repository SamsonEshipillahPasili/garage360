from django import forms

class CreateBookingForm(forms.Form):
    car_brand = forms.CharField(max_length=255)
    car_model = forms.CharField(max_length=255)
    car_number_plate = forms.CharField(max_length=255)
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

