from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton


from accounts.forms import UserProfileForm
from accounts.models import UserProfile


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

class CreateUserProfileView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm

    def form_valid(self, form: UserProfileForm):
        is_staff = form.cleaned_data.get('is_staff') == 'true'

        if is_staff:
            UserProfile.objects.create_staff(
                organization=self.request.user.profile.organization,
                **form.cleaned_data
            )
        else:
            UserProfile.objects.create_client(
                organization=self.request.user.profile.organization,
                **form.cleaned_data
            )

        entity = 'Staff' if is_staff else 'Client'
        messages.info(self.request, f'{entity} created successfully')
        return HttpResponseRedirect(
            reverse_lazy('accounts:list_profiles', query={'is_staff': True})
        )

class ListProfilesView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        is_staff = self.request.GET.get('is_staff', 'false') == 'true'
        filter_ = {'is_staff': True} if is_staff else {'is_client': True}

        return (
            UserProfile.objects
            .filter(
                **filter_,
                organization=self.request.user.profile.organization
            )
            .select_related('user')
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileForm()
        return context

class EditProfileView(LoginRequiredMixin, View):

    def get_queryset(self):
        return (
            UserProfile.objects
            .filter(
                organization=self.request.user.profile.organization
            )
            .select_related('user')
            .all()
        )

    def get(self, request, pk: int):
        client = get_object_or_404(self.get_queryset(), pk=pk)

        initial = {
            'email': client.user.email,
            'first_name': client.user.first_name,
            'last_name': client.user.last_name,
            'phone_number': client.phone_number,
        }
        form = UserProfileForm(initial=initial)
        context = {
            'client': client,
            'form': form,
        }
        return render(request, 'accounts/profile_detail.html', context)

    def post(self, request, pk: int):
        profile = get_object_or_404(self.get_queryset(), pk=pk)

        form = UserProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'profile': profile,
                'form': form,
            }
            return render(request, 'accounts/profile_detail.html', context)

        UserProfile.objects.update_profile(
            instance=profile,
            **form.cleaned_data,
        )
        messages.info(self.request, 'Profile updated successfully')
        return HttpResponseRedirect(reverse_lazy('accounts:profiles'))

