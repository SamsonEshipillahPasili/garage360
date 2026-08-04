from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from django.views.generic import TemplateView, ListView

from accounts.models import UserProfile
from .forms import CreateBookingForm, CreateQuotationItemForm
from .models import Booking, Quotation


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


class ListAllBookingsView(LoginRequiredMixin, ListView):
    template_name = 'core/list_all_bookings.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_item'] = 'list_all_bookings'
        return context

    def get_queryset(self) -> QuerySet[Booking]:
        return (
            Booking.objects
                .select_related('client__user')
                .filter(client__organization=self.request.user.profile.organization)
        )


class BookingDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, booking_id: int):
        qs = (
            Booking.objects
                .select_related('client__organization', 'quotation')
                .prefetch_related('quotation__quotation_lines')
        )
        booking = get_object_or_404(qs, pk=booking_id)
        if booking.client.organization.id != request.user.profile.organization.id:
            raise Http404

        context = {
            'booking': booking,
            'quotation_item_form': CreateQuotationItemForm(),
        }
        return render(request, 'core/booking_detail.html', context)


class CreateQuotationItemView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, quotation_id: int):
        quotation_qs = Quotation.objects.select_related('booking__created_by__organization')

        # ensure the quotation exists.
        quotation = get_object_or_404(quotation_qs, pk=quotation_id)

        # ensure the booking status is not terminal
        if quotation.booking.status not in (Booking.BookingStatus.PENDING, Booking.BookingStatus.IN_PROGRESS):
            raise Http404

        # ensure the booking was created by a member of the same org
        if quotation.booking.created_by.organization.id != request.user.profile.organization.id:
            raise Http404

        form = CreateQuotationItemForm(request.POST)
        if form.is_valid():
            form.save(quotation=quotation)
            messages.info(request, 'Quotation was created successfully')
            return HttpResponseRedirect(reverse('core:booking_detail', kwargs={'booking_id': quotation.booking.id}))

        context = {
            'booking': quotation.booking,
            'quotation_item_form': form
        }
        return render(request, 'core/booking_detail.html', context)
