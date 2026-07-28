from django import forms

class CreateClientForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
