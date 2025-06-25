from django.urls import path
from .views import hello_apiview

app_name = 'tasks'
urlpatterns = [
    path(
        'hello/',
        hello_apiview,
        name='hello',
    )
]
