from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Предоставление доступа к задачам их владельцу."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_staff \
            or obj.user == request.user

class IsStaff(permissions.BasePermission):
    """Предоставление доступа к задачам персоналу."""

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff
