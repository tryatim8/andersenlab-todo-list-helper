from typing import TYPE_CHECKING
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Task


if TYPE_CHECKING:
    ModelAdminClass = ModelAdmin[Task]
else:
    ModelAdminClass = ModelAdmin


@admin.register(Task)
class TaskModelAdmin(ModelAdminClass):
    """Task model display for the admin panel."""

    list_display = ['pk', 'title', 'user', 'status', 'description_short']
    list_display_links = ['pk', 'title', 'status']
    ordering = ['-pk', 'status']

    def description_short(self, obj: Task) -> str:
        """Короткое описание задачи."""

        if not obj.description:
            return ''
        elif len(obj.description) <= 60:
            return obj.description
        else:
            return obj.description[:57] + '...'
