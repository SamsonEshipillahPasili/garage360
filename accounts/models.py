import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

##############################################
# Managers                                   #
##############################################

class UserProfileManager(models.Manager):
    def create_client(
          self,
          organization: 'Organization',
          email: str,
          first_name: str,
          last_name: str,
          phone_number: str
        ) -> 'UserProfile':

        return self._create_profile(
            organization=organization,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_admin=False,
            is_staff=False,
            is_client=True
        )

    def create_staff(
            self,
            organization: 'Organization',
            email: str,
            first_name: str,
            last_name: str,
            phone_number: str,
    ) -> 'UserProfile':

        return self._create_profile(
            organization=organization,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_admin=False,
            is_staff=True,
            is_client=False
        )

    def create_admin(
             self,
             organization: 'Organization',
             email: str,
             first_name: str,
             last_name: str,
             phone_number: str,
    ) -> 'UserProfile':

        return self._create_profile(
            organization=organization,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_admin=True,
            is_staff=False,
            is_client=False
        )

    def _create_profile(
            self,
            organization: 'Organization',
            email: str,
            first_name: str,
            last_name: str,
            phone_number: str,
            is_admin: bool,
            is_staff: bool,
            is_client: bool,
    ) -> 'UserProfile':

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

            # then create the profile
            return UserProfile.objects.create(
                organization=organization,
                user=user,
                phone_number=phone_number,
                is_admin=is_admin,
                is_staff=is_staff,
                is_client=is_client,
            )

    def update_profile(
            self,
            instance: 'UserProfile',
            email: str,
            first_name: str,
            last_name: str,
            phone_number: str
    ):
        with transaction.atomic():
            instance.user.email = email
            instance.user.first_name = first_name
            instance.user.last_name = last_name
            instance.user.save(update_fields=["email", "first_name", "last_name"])

            instance.phone_number = phone_number
            instance.save(update_fields=["phone_number"])

##############################################
# Models                                     #
##############################################

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Organization(TimestampedModel):
    name = models.CharField(max_length=255)

class UserProfile(TimestampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    is_password_set = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    objects = UserProfileManager()

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
            self.save(update_fields=["password"])
