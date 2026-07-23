from django.db import models
from django.contrib.auth.models import User

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Client(TimestampedModel):
    phone_number = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Vehicle(TimestampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    yom = models.PositiveIntegerField()
    number_plate = models.CharField(max_length=255)
