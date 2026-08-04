from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('booking/create/<int:profile_id>', views.CreateBookingView.as_view(), name='create_booking'),
    path('booking/all', views.ListAllBookingsView.as_view(), name='list_bookings'),
    path('booking/<int:booking_id>', views.BookingDetailView.as_view(), name='booking_detail'),
    path(
        '/quotation/create_line/<int:quotation_id>',
        views.CreateQuotationItemView.as_view(),
        name='create_quotation_line'
    ),
    path(
        '/quotation/delete_line/<int:line_id>',
        views.DeleteQuotationLineView.as_view(),
         name='delete_quotation_line'
    ),
]
