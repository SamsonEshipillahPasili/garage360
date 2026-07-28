from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

class CreateClientForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            "email",
            "first_name",
            "last_name",
            "phone",
            Submit("submit", "Create Client"),
        )
