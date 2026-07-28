from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import CreateClientForm
from .models import Client


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

class CreateClientView(LoginRequiredMixin, FormView):
    template_name = 'core/create_client.html'
    form_class = CreateClientForm
    success_url = reverse_lazy('core:create_client')

    def form_valid(self, form: CreateClientForm):
        Client.objects.create_client(
            **form.cleaned_data
        )
        messages.info(self.request, 'Client created successfully')
        return super().form_valid(form)


class ListClientsView(LoginRequiredMixin, ListView):
    template_name = 'core/list_clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.select_related('user').all()

