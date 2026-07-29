from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import CreateClientForm
from .models import Client


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

class CreateClientView(LoginRequiredMixin, FormView):
    form_class = CreateClientForm
    success_url = reverse_lazy('core:list_clients')

    def form_valid(self, form: CreateClientForm):
        Client.objects.create_client(
            **form.cleaned_data
        )
        messages.info(self.request, 'Client created successfully')
        return super().form_valid(form)


class ListClientsView(LoginRequiredMixin, ListView):
    template_name = 'core/clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.select_related('user').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_client_form'] = CreateClientForm()
        return context


class EditClientView(LoginRequiredMixin, View):

    def get_queryset(self):
        return Client.objects.select_related('user').all()

    def get(self, request, pk: int):
        client = get_object_or_404(self.get_queryset(), pk=pk)

        initial_form_data = {
            'email': client.user.email,
            'first_name': client.user.first_name,
            'last_name': client.user.last_name,
            'phone': client.phone_number,
        }
        form = CreateClientForm(initial=initial_form_data)
        context = {
            'client': client,
            'form': form,
        }
        return render(request, 'core/client_detail.html', context)

    def post(self, request, pk: int):
        client = get_object_or_404(self.get_queryset(), pk=pk)

        form = CreateClientForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'client': client,
                'form': form,
            }
            return render(request, 'core/client_detail.html', context)

        Client.objects.update_client(
            instance=client,
            **form.cleaned_data
        )
        messages.info(self.request, 'Client updated successfully')
        return HttpResponseRedirect(reverse_lazy('core:list_clients'))
