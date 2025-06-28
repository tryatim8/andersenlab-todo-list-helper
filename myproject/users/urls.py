from django.urls import path
from .views import hello_apiview

app_name = 'users'
urlpatterns = [
    path(
        'hello/',
        hello_apiview,
        name='hello',
    )
]
