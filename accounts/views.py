from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AuthLoginView(LoginView):
    template_name = 'accounts/login.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'
