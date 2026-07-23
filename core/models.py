from django.db import models

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(TimestampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()

class Vehicle(TimestampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    yom = models.PositiveIntegerField()
    number_plate = models.CharField(max_length=255)
