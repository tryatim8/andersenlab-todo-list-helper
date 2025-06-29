import random

import pytest
from rest_framework import status

from tasks.models import Task
from tasks.serializers import TaskSerializer



@pytest.mark.django_db
def test_tasks_list_failed(api_client, tasks_serialized, user):
    response = api_client.get('/api/tasks/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data


@pytest.mark.django_db
@pytest.mark.parametrize('page_num', [1, 2])
def test_tasks_list_successful_with_pagination(
        auth_client, tasks_serialized, page_size, page_num,
    ):
    response = auth_client.get('/api/tasks/', query_params={'page': page_num})
    assert response.status_code == status.HTTP_200_OK
    assert list(response.data.keys()) == ['count', 'next', 'previous', 'results']
    assert response.data['count'] == len(tasks_serialized)
    start = (page_num - 1) * page_size
    assert response.data['results'] == tasks_serialized[start:start+page_size]


@pytest.mark.django_db
@pytest.mark.parametrize('task_status', ['new', 'in_progress', 'completed'])
def test_tasks_list_with_status_filter(
        auth_client, tasks_serialized, page_size, task_status,
    ):
    response = auth_client.get('/api/tasks/', query_params={'status': task_status})
    assert response.status_code == status.HTTP_200_OK
    expected_tasks = [t for t in tasks_serialized if t['status'] == task_status]
    assert response.data['count'] == len(expected_tasks)
    assert response.data['results'] == expected_tasks[:page_size]


@pytest.mark.django_db
def test_task_detail_successful(auth_client, tasks_serialized):
    tasks_sample = random.choices(tasks_serialized, k=3)
    for task in tasks_sample:
        task_pk = task['pk']
        response = auth_client.get(f'/api/tasks/{task_pk}/')
        assert response.status_code == status.HTTP_200_OK
        expected_task = Task.objects.get(pk=task['pk'])
        assert response.data == TaskSerializer(expected_task).data

@pytest.mark.django_db
def test_task_create_successful(auth_client, user):
    response_data = {
        'title': 'example_task',
        'description': 'Example text task description',
    }
    response = auth_client.post('/api/tasks/', data=response_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = Task.objects.get(pk=response.data['pk'])
    assert created_task.title == response_data['title']
    assert created_task.description == response_data['description']
    assert created_task.user == user
    assert created_task.status == 'new'

