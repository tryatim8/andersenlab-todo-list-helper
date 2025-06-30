from typing import Optional, Any

from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from .serializers import TaskSerializer
from .models import Task
from .permissions import IsOwner, IsStaff


class TasksListApiView(ListAPIView[Task]):
    """Retrieve a list of all users' tasks."""

    serializer_class = TaskSerializer
    permission_classes = [IsStaff]
    filterset_fields = ['status']

    def get_queryset(self) -> QuerySet[Task]:
        return Task.objects.select_related('user').order_by('-pk')


@extend_schema_view(
    retrieve=extend_schema(parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH)
    ])
)
class TasksApiViewSet(ModelViewSet[Task]):
    """
    ModelViewSet managing tasks of the authenticated user..

    Provides actions to list, retrieve, create, update, delete tasks,
    and mark them as completed. Access is restricted to the task owner.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ['status']

    def get_queryset(self) -> QuerySet[Task]:
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) \
                or isinstance(user, AnonymousUser):
            return Task.objects.none()  # safe fake queryset
        return Task.objects.filter(user=user) \
            .select_related('user').order_by('-pk')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='status',
                description='- `new` - New task\n'
                            '- `in_progress` - In progress\n'
                            '- `completed` - Completed',
                enum=['new', 'in_progress', 'completed'],
            ),
        ]
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer: BaseSerializer[Task]) -> None:
        serializer.save(user=self.request.user)

    def perform_update(self, serializer: BaseSerializer[Task]) -> None:
        serializer.save()

    def destroy(
        self, request: Request, *args: Any, **kwargs: Any,
    ) -> Response:
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def mark_completed(
        self, request: Request, pk: Optional[int] = None,
    ) -> Response:
        """Mark the task as completed."""

        task = self.get_object()
        if task.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
