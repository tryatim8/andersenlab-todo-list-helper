import pytest
from rest_framework import status

from tasks.serializers import TaskSerializer


@pytest.mark.django_db
def test_tasks_list_failed(api_client, tasks_list, user):
    response = api_client.get('/api/tasks/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data


@pytest.mark.django_db
def test_tasks_list_successful(auth_client, tasks_list):
    response = auth_client.get('/api/tasks/')
    assert response.status_code == status.HTTP_200_OK
    assert list(response.data.keys()) == ['count', 'next', 'previous', 'results']
    assert response.data['count'] == len(tasks_list)
    assert response.data['results'] == [
        TaskSerializer(task).data for task
        in sorted(tasks_list, key=lambda elem: -elem.pk)
    ]
