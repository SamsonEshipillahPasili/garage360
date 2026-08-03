from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from django.views.generic import TemplateView

from accounts.models import UserProfile
from .forms import CreateBookingForm
from .models import Booking


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


class CreateBookingView(LoginRequiredMixin, View):

    def _get_template_name(self) -> str:
        return 'core/create_booking.html'

    def _get_user_profile_qs(self, request: HttpRequest) -> QuerySet:
        return (
            UserProfile.objects
                .select_related('user')
                .filter(
                    organization=request.user.profile.organization,
                )
        )

    def _get_bookings(self, client: UserProfile) -> QuerySet[Booking]:
        return Booking.objects.filter(
            client=client
        )

    def get(self, request: HttpRequest, profile_id: int):
        qs = self._get_user_profile_qs(request=request)
        user_profile = get_object_or_404(qs, pk=profile_id)
        bookings = self._get_bookings(user_profile)

        booking_form = CreateBookingForm()

        context = {
            'profile': user_profile,
            'booking_form': booking_form,
            'bookings': bookings,
        }
        return render(request, self._get_template_name(), context)

    def post(self, request: HttpRequest, profile_id: int):
        qs = self._get_user_profile_qs(request=request)
        user_profile = get_object_or_404(qs, pk=profile_id)

        booking_form = CreateBookingForm(request.POST)
        if booking_form.is_valid():
            booking_form.save(
                client=user_profile,
                created_by=request.user.profile,
            )
            messages.info(request, 'Booking was created successfully')
            return HttpResponseRedirect(
                reverse('core:create_booking', kwargs={'profile_id': profile_id})
            )
        else:
            messages.error(request, 'Error creating booking')
            context = {
                'profile': user_profile,
                'booking_form': booking_form,
                'bookings': self._get_bookings(user_profile),
            }
            return render(request, self._get_template_name(), context)
