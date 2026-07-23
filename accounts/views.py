from django.contrib.auth.views import LoginView

class AuthLoginView(LoginView):
    template_name = 'accounts/login.html'

