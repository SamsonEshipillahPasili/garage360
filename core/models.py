import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClientManager(models.Manager):

    def update_client(
            self, instance: 'Client',  email: str, first_name: str, last_name: str, phone: str
    ) -> 'Client':
        with transaction.atomic():
            instance.user.email = email
            instance.user.first_name = first_name
            instance.user.last_name = last_name
            instance.user.save()

            instance.phone_number = phone
            instance.save()

    def create_client(
            self, email: str, first_name: str, last_name: str, phone: str
    ) -> 'Client':
        # open a transaction
        with transaction.atomic():
            # initial password
            pwd = uuid.uuid4().hex

            # first create the user
            user = User.objects.create_user(
                email=email,
                password=pwd,
                first_name=first_name,
                last_name=last_name,
                username=email,
            )

            # then create the client
            return Client.objects.create(user=user, phone_number=phone)


class Client(TimestampedModel):
    phone_number = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_password_set = models.BooleanField(default=False)

    def set_password(self, password: str):
        """
        Set password for this client for first time logins.
        Further attempts will throw an error.
        """
        if self.is_password_set:
            raise ValueError(f"Password is already set for user: {self.user.username}")

        with transaction.atomic():
            self.user.set_password(password)
            self.user.save(update_fields=["password"])
            self.is_password_set = True
            self.save()

    objects = ClientManager()

class Vehicle(TimestampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    yom = models.PositiveIntegerField()
    number_plate = models.CharField(max_length=255)
