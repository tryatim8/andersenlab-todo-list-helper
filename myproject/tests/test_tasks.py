import random

import pytest
from rest_framework import status

from tasks.models import Task
from tasks.serializers import TaskSerializer


@pytest.mark.django_db
def test_tasks_list_failed(api_client, tasks_serialized, user):
    """Unauthorized user cannot access tasks list."""
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
    assert list(response.data.keys()) == [
        'count', 'next', 'previous', 'results',
    ]
    assert response.data['count'] == len(tasks_serialized)
    start = (page_num - 1) * page_size
    assert response.data['results'] == tasks_serialized[start:start+page_size]


@pytest.mark.django_db
@pytest.mark.parametrize('task_status', ['new', 'in_progress', 'completed'])
def test_tasks_list_with_status_filter(
    auth_client, tasks_serialized, page_size, task_status,
):
    """Filter tasks list by status."""
    response = auth_client.get(
        '/api/tasks/',
        query_params={'status': task_status},
    )
    assert response.status_code == status.HTTP_200_OK
    expected_tasks = [t for t in tasks_serialized if t['status'] == task_status]
    assert response.data['count'] == len(expected_tasks)
    assert response.data['results'] == expected_tasks[:page_size]


@pytest.mark.django_db
def test_task_detail_by_pk_successful(auth_client, tasks_list):
    for task in random.sample(tasks_list, k=3):
        task_pk = task.pk
        response = auth_client.get(f'/api/tasks/{task_pk}/')
        assert response.status_code == status.HTTP_200_OK
        expected_task = Task.objects.get(pk=task.pk)
        assert response.data == TaskSerializer(expected_task).data


@pytest.mark.django_db
@pytest.mark.parametrize('task_pk', [0, -12, 10 ** 10])
def test_task_detail_by_pk_failed(auth_client, tasks_list, task_pk):
    response = auth_client.get(f'/api/tasks/{task_pk}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Task matches the given query.'


@pytest.mark.django_db
def test_task_create_successful(auth_client, user):
    """Create a new task with default status 'new'."""
    response_data = {
        'title': 'example_task',
        'description': 'Example text for the task description',
    }
    response = auth_client.post('/api/tasks/', data=response_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = Task.objects.get(pk=response.data['pk'])
    assert created_task.title == response_data['title']
    assert created_task.description == response_data['description']
    assert created_task.user == user
    assert created_task.status == 'new'


@pytest.mark.django_db
def test_task_full_change_by_id_successful(auth_client, tasks_serialized):
    """Full update of multiple tasks by ID."""
    response_data = {
        'title': 'example_task',
        'description': 'Example text for the task description',
        'status': 'in_progress',
    }
    tasks_to_change = random.sample(tasks_serialized, k=3)
    for task in tasks_to_change:
        task_pk = task['pk']
        response = auth_client.put(f'/api/tasks/{task_pk}/', data=response_data)
        assert response.status_code == status.HTTP_200_OK
        task.update(response_data)
        expected_task = Task.objects.get(pk=task_pk)
        assert task == TaskSerializer(expected_task).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('title', 'new_status'),
    [('one', 'in_progress'), ('two', 'completed')],
)
def test_task_change_partly_by_id_successful(
    auth_client, tasks_serialized, title, new_status,
):
    """Partial update of a task by ID."""
    response_data = {'title': title, 'status': new_status}
    task_to_change = random.choice(tasks_serialized)
    task_pk = task_to_change['pk']
    response = auth_client.patch(f'/api/tasks/{task_pk}/', data=response_data)
    assert response.status_code == status.HTTP_200_OK
    task_to_change.update(response_data)
    expected_task = Task.objects.get(pk=task_pk)
    assert task_to_change == TaskSerializer(expected_task).data


@pytest.mark.django_db
def test_task_delete_by_id_successful(auth_client, tasks_serialized):
    for task in random.sample(tasks_serialized, k=3):
        task_pk = task['pk']
        response = auth_client.delete(f'/api/tasks/{task_pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        deleted_task = Task.objects.filter(pk=task_pk)
        assert not deleted_task.exists()


@pytest.mark.django_db
@pytest.mark.parametrize('task_pk', [0, -123, 10 ** 10])
def test_task_delete_by_id_failed(auth_client, tasks_serialized, task_pk):
    response = auth_client.delete(f'/api/tasks/{task_pk}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Task matches the given query.'


@pytest.mark.django_db
def test_task_mark_completed_by_id_successful(auth_client, tasks_serialized):
    """Mark tasks as completed by ID."""
    for task in random.sample(tasks_serialized, k=3):
        task_pk = task['pk']
        response = auth_client.post(f'/api/tasks/{task_pk}/mark_completed/')
        assert response.status_code == status.HTTP_200_OK
        task.update({'status': 'completed'})
        expected_task = Task.objects.get(pk=task_pk)
        assert task == TaskSerializer(expected_task).data == response.data


@pytest.mark.django_db
@pytest.mark.parametrize('task_pk', [0, -123, 10 ** 10])
def test_task_mark_completed_by_id_failed(
    auth_client, tasks_serialized, task_pk,
):
    response = auth_client.post(f'/api/tasks/{task_pk}/mark_completed/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Task matches the given query.'


@pytest.mark.django_db
@pytest.mark.parametrize('page_num', [1, 2])
def test_all_tasks_list_with_pagination_via_superuser_client_successful(
    superuser_client, tasks_serialized, page_size, page_num,
):
    response = superuser_client.get(
        '/api/tasks/all/', query_params={'page': page_num},
    )
    assert response.status_code == status.HTTP_200_OK
    assert list(response.data.keys()) == [
        'count', 'next', 'previous', 'results',
    ]
    assert response.data['count'] == len(tasks_serialized)
    start = (page_num - 1) * page_size
    assert response.data['results'] == tasks_serialized[start:start + page_size]


@pytest.mark.django_db
def test_all_tasks_list_from_user_client_failed(auth_client, tasks_serialized):
    """Regular user cannot access all tasks list."""
    response = auth_client.get('/api/tasks/all/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert 'detail' in response.data
    assert response.data['detail'] == ('You do not have permission to perform '
                                       'this action.')
