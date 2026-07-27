from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

class AuthLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            StrictButton('Login', css_class='btn btn-primary', type='submit'),
        )

class AuthLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthLoginForm


