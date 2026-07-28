from core.models import Client
from core.models import User

def test_can_correctly_create_client(db):
    """
    Verify that create_client() creates a Client and associated User
    with the expected personal details.

    The created User should have its email and username set to the
    supplied email address, and the Client should store the provided
    phone number.
    """
    assert not Client.objects.exists()
    assert not User.objects.exists()

    email = "client@gmail.com"
    first_name = "CFName"
    last_name = "CLName"
    phone = "+5757767676"

    client = Client.objects.create_client(
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

    assert Client.objects.count() == 1
    assert User.objects.count() == 1

