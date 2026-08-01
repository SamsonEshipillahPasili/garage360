from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('booking/create/<int:profile_id>', views.CreateBookingView.as_view(), name='create_booking'),
]
