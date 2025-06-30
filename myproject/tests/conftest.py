import random
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from faker import Faker
from rest_framework.test import APIClient
import pytest
from rest_framework.utils.serializer_helpers import ReturnDict

from tasks.models import Task
from tasks.serializers import TaskSerializer


User = get_user_model()
fake = Faker()

if TYPE_CHECKING:
    from users.models import User as UserType


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db: Any) -> UserType:
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
    )


@pytest.fixture
def user_credentials(user: UserType) -> Dict[str, str]:
    return {'username': 'testuser', 'password': 'testpass123'}


@pytest.fixture
def access_token(
    api_client: APIClient, user_credentials: Dict[str, str], user: UserType,
) -> str:
    """Returns JWT access token."""
    response = api_client.post('/api/token/', data=user_credentials)
    assert response.status_code == 200, \
        f"Failed to get access token: {response.data}"
    assert 'access' in response.data, "Access token missing in response"
    access: str = response.data['access']
    return access


@pytest.fixture
def refresh_token(
    api_client: APIClient, user_credentials: Dict[str, str], user: UserType,
) -> str:
    """Returns JWT refresh token."""
    response = api_client.post('/api/token/', data=user_credentials)
    assert response.status_code == 200, \
        f"Failed to get refresh token: {response.data}"
    assert 'refresh' in response.data, "Refresh token missing in response"
    refresh: str = response.data['refresh']
    return refresh


@pytest.fixture
def auth_client(
    api_client: APIClient, access_token: str, user: UserType,
) -> APIClient:
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client


@pytest.fixture
def access_token_refreshed(
    api_client: APIClient, refresh_token: str, user: UserType,
) -> str:
    """Returns refreshed access token."""
    response = api_client.post(
        '/api/token/refresh/',
        data={'refresh': refresh_token},
    )
    assert response.status_code == 200, \
        f"Failed to refresh access token: {response.data}"
    assert 'access' in response.data, \
        "Refreshed access token missing in response"
    access: str = response.data['access']
    return access


@pytest.fixture
def auth_client_refreshed(
    api_client: APIClient, access_token_refreshed: str, user: UserType,
) -> APIClient:
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {access_token_refreshed}',
    )
    return api_client


@pytest.fixture
def tasks_list(user: UserType) -> List[Task]:
    """Creates and returns a list of tasks."""
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
def tasks_serialized(tasks_list: List[Task]) -> List[ReturnDict[str, Any]]:
    return [TaskSerializer(task).data for task in tasks_list]


@pytest.fixture
def page_size() -> Optional[int]:
    size: object = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)
    return int(size) if isinstance(size, (int, str)) else None


@pytest.fixture
def superuser(db: Any) -> UserType:
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
    )


@pytest.fixture
def superuser_client(superuser: UserType, api_client: APIClient) -> APIClient:
    api_client.force_authenticate(user=superuser)
    return api_client
