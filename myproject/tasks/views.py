from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer

from .models import Task
from .permissions import IsOwner, IsStaff


class TasksListApiView(ListAPIView):
    """Получение списка задач всех пользователей."""

    serializer_class = TaskSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        return Task.objects.select_related('user').order_by('pk')


class TasksApiViewSet(ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user) \
            .select_related('user').order_by('-pk')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Отметить задачу как выполненную."""

        task = self.get_object()
        if task.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
