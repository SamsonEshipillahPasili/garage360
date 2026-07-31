# from django.db import models
# from django.utils import timezone
#
# from accounts.models import UserProfile
#
# class Diagnostic(models.Model):
#     ...
#
# class Booking(models.Model):
#     user_profile = models.ForeignKey(
#         UserProfile,
#         on_delete=models.CASCADE,
#         related_name='bookings'
#     )
#     car_brand = models.CharField(max_length=255)
#     car_model = models.CharField(max_length=255)
#     car_yom = models.CharField(max_length=255)
#     car_number_plate = models.CharField(max_length=255)
#     booking_date = models.DateField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
