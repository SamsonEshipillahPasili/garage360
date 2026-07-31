from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is taken!")
