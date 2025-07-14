from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


class RegisterApiView(CreateAPIView[User]):
    """Registering a new user."""

    permission_classes = [AllowAny]
    serializer_class = UserSerializer
