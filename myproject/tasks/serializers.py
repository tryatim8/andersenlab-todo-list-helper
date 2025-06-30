from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task
from users.serializers import UserSerializer


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer[Task]):
    """Сериализатор данных сущности задачи."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['pk', 'title', 'description', 'status', 'user']
