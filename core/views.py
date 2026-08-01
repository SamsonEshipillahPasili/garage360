from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View

from django.views.generic import TemplateView

from accounts.models import UserProfile
from .forms import CreateBookingForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


class CreateBookingView(LoginRequiredMixin, View):

    def _get_user_profile_qs(self, request: HttpRequest) -> QuerySet:
        return (
            UserProfile.objects
                .select_related('user')
                .filter(
                    organization=request.user.profile.organization,
                )
        )

    def get(self, request: HttpRequest, profile_id: int):
        qs = self._get_user_profile_qs(request=request)
        user_profile = get_object_or_404(qs, pk=profile_id)

        booking_form = CreateBookingForm()

        context = {
            'profile': user_profile,
            'booking_form': booking_form,
        }
        return render(request, 'core/create_booking.html', context)

