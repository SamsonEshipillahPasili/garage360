from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .models import  UserProfile


class UserProfileForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=255)
    instance: UserProfile = None

    def set_instance(self, instance: UserProfile):
        self.instance = instance

    def clean_email(self):
        email = self.cleaned_data['email']

        if not self.instance:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email is taken!")
        else:
            existing_user = self.instance.user
            if User.objects.filter(email=email).filter(~Q(id=existing_user.id)).exists():
                raise forms.ValidationError("Email is taken!")

        return email
