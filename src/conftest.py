import pytest

from app.models import User


@pytest.fixture
def test_password():
    return "a_simple_password"


@pytest.fixture
def user(db, test_password):
    user = User.objects.create(
        first_name="Johnny", last_name="McMahon", email="johnny@social.com", is_staff=True)

    user.set_password(test_password)
    user.save()

    return user


# for unauthorized requests
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


# for authorized requests
@pytest.fixture
def api_client_with_token(db, user, api_client):
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
