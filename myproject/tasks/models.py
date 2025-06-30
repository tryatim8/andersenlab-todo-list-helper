from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    """Task model for the database."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks',
    )
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        default='new',
        choices=[
            ('new', 'New'),
            ('in_progress', 'In progress'),
            ('completed', 'Completed'),
        ],
    )

    def __str__(self):
        return f'Task `{self.title}` is {self.status}'
