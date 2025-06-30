from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    """Task model display for the admin panel."""

    list_display = ['pk', 'title', 'user', 'status', 'description_short']
    list_display_links = ['pk', 'title', 'status']
    ordering = ['-pk', 'status']

    @classmethod
    def description_short(cls, obj: Task):
        """Короткое описание задачи."""

        if not obj.description:
            return ''
        elif len(obj.description) <= 60:
            return obj.description
        else:
            return obj.description[:57] + '...'
