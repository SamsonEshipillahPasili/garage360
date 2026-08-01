from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView

from accounts.models import UserProfile


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


class CreateBookingView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, profile_id: int):
        qs = UserProfile.objects.select_related('user').filter(
            organization=request.user.profile.organization,
        )
        user_profile = get_object_or_404(qs, pk=profile_id)

        context = {
            'profile': user_profile,
        }
        return render(request, 'core/create_booking.html', context)
