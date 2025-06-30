from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    """Serializer for the User model."""

    password = serializers.CharField(
        write_only=True, validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data: Dict[str, Any]) -> UserType:
        """Create and return a new user with encrypted password."""

        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user
