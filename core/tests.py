import pytest

from faker import Faker
from accounts.models import UserProfile
from django.contrib.auth.models import User

fake = Faker()

@pytest.fixture
def client_user(db):
   return UserProfile.objects.create_client(
        email="client@gmail.com",
        first_name="CFName",
        last_name="CLName",
        phone="+5757767676"
    )

@pytest.mark.django_db
def test_can_correctly_create_client():
    assert not UserProfile.objects.exists()
    assert not User.objects.exists()

    email = "client@gmail.com"
    first_name = "CFName"
    last_name = "CLName"
    phone = "+5757767676"

    client = UserProfile.objects.create_client(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )

    user = client.user

    assert client.phone_number == phone
    assert not client.is_password_set

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.username == email

    assert UserProfile.objects.count() == 1
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_client_password_is_set_correctly():
    client = UserProfile.objects.create_client(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
    )
    assert not client.is_password_set
    new_password = fake.password(length=10)
    client.set_password(new_password)
    assert client.is_password_set
    assert client.user.check_password(new_password)


@pytest.mark.django_db
def test_client_can_be_updated_correctly(client_user):
    new_client_data = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone': fake.phone_number(),
    }

    assert new_client_data['first_name'] != client_user.user.first_name
    assert new_client_data['last_name'] != client_user.user.last_name
    assert new_client_data['email'] != client_user.user.email
    assert new_client_data['phone'] != client_user.phone_number

    UserProfile.objects.update_profile(
        instance=client_user,
        **new_client_data
    )

    assert new_client_data['first_name'] == client_user.user.first_name
    assert new_client_data['last_name'] == client_user.user.last_name
    assert new_client_data['email'] == client_user.user.email
    assert new_client_data['phone'] == client_user.phone_number

