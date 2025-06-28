from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TasksListApiView, TasksApiViewSet

router = DefaultRouter()
router.register('', TasksApiViewSet, basename='task')

app_name = 'tasks'
urlpatterns = [
    path('all/', TasksListApiView.as_view(), name='all_tasks'),
    path('', include(router.urls)),
]
