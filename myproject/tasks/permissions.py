from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Task


class IsOwner(permissions.BasePermission):
    """Permission class that grants access to the task owner."""

    def has_object_permission(
            self, request: Request, view: APIView, obj: Task,
    ) -> bool:
        return request.user.is_superuser or request.user.is_staff \
            or obj.user == request.user


class IsStaff(permissions.BasePermission):
    """Permission class that grants access to the staff."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_superuser or request.user.is_staff
