import pytest
from rest_framework import status

@pytest.mark.django_db
def test_successful_login_returns_tokens(api_client, user_credentials):
    response = api_client.post('/api/token/', data=user_credentials)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_failed_login_returning_forbidden(api_client):
    response = api_client.post(
        '/api/token/',
        data={'username': 'wrong_username', 'password': 'wrong_password'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'detail' in response.data

@pytest.mark.django_db
def test_access_fail_without_token(api_client):
    response = api_client.get('/api/tasks/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'results' not in response.data
    assert 'detail' in response.data

@pytest.mark.django_db
@pytest.mark.parametrize('client_name', ['auth_client', 'auth_client_refreshed'])
def test_access_successful_with_token(request, client_name):
    response = request.getfixturevalue(client_name).get('/api/tasks/')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
