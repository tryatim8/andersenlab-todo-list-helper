from typing import Dict

import pytest
from _pytest.fixtures import SubRequest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from users.serializers import UserSerializer

User = get_user_model()


@pytest.mark.django_db
def test_successful_login_returns_tokens(
    api_client: APIClient, user_credentials: Dict[str, str],
) -> None:
    """Login returns access and refresh tokens."""
    response = api_client.post('/api/token/', data=user_credentials)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_failed_login_returning_forbidden(api_client: APIClient) -> None:
    response = api_client.post(
        '/api/token/',
        data={'username': 'wrong_username', 'password': 'wrong_password'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'detail' in response.data


@pytest.mark.django_db
def test_access_fail_without_token(api_client: APIClient) -> None:
    response = api_client.get('/api/tasks/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'results' not in response.data
    assert 'detail' in response.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name',
    ['auth_client', 'auth_client_refreshed'],
)
def test_access_successful_with_token(
    request: SubRequest, client_name: str,
) -> None:
    """Access granted with valid authentication token."""
    response = request.getfixturevalue(client_name).get('/api/tasks/')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data


@pytest.mark.django_db
def test_register_user_successful(
   api_client: APIClient, new_user_credentials: Dict[str, str]
) -> None:
    response = api_client.post(
        '/api/users/register/',
        data=new_user_credentials,
    )
    assert response.status_code == status.HTTP_201_CREATED
    new_user = User.objects.get(username=new_user_credentials['username'])
    assert response.data == UserSerializer(instance=new_user).data


@pytest.mark.django_db
def test_register_user_failed_no_password(
    api_client: APIClient, new_user_credentials: Dict[str, str]
) -> None:
    new_user_credentials.pop('password')
    assert 'password' not in new_user_credentials, 'The password exists'
    response = api_client.post(
        '/api/users/register/',
        data=new_user_credentials,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'This field is required.' in response.data['password']
