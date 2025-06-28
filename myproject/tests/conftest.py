import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
    )

@pytest.fixture
def user_credentials(user):
    return {'username': 'testuser', 'password': 'testpass123'}

@pytest.fixture
def access_token(api_client, user_credentials, user):
    response = api_client.post('/api/token/', data=user_credentials)
    return response.data['access']

@pytest.fixture
def refresh_token(api_client, user_credentials, user):
    response = api_client.post('/api/token/', data=user_credentials)
    return response.data['refresh']

@pytest.fixture
def auth_client(api_client, access_token, user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client

@pytest.fixture
def access_token_refreshed(api_client, refresh_token, user):
    response = api_client.post('/api/token/refresh/', data={'refresh': refresh_token})
    return response.data['access']

@pytest.fixture
def auth_client_refreshed(api_client, access_token_refreshed, user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_refreshed}')
    return api_client
