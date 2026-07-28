from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

import logzero

from .forms import CreateClientForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

class CreateClientView(LoginRequiredMixin, FormView):
    template_name = 'core/create_client.html'
    form_class = CreateClientForm
    success_url = reverse_lazy('core:create_client')

    def form_valid(self, form: CreateClientForm):
        logzero.logger.info(form.cleaned_data)
        messages.info(self.request, 'Client created successfully')
        return super().form_valid(form)
