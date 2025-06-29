import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from faker import Faker
from rest_framework.test import APIClient
import pytest

from tasks.models import Task
from tasks.serializers import TaskSerializer


User = get_user_model()
fake = Faker()


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

@pytest.fixture
def tasks_list(user):
    with atomic():
        tasks = [
            Task.objects.create(
                user=user,
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=3),
                status=random.choice(['new', 'in_progress', 'completed']),
            )
            for _ in range(15)
        ]
    return list(sorted(tasks, key=lambda t: -t.pk))

@pytest.fixture
def tasks_serialized(tasks_list):
    return [TaskSerializer(task).data for task in tasks_list]

@pytest.fixture
def page_size():
    return settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)

@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
    )
@pytest.fixture
def superuser_client(superuser, api_client):
    api_client.force_authenticate(user=superuser)
    return api_client
