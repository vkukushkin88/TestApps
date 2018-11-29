from rest_framework import permissions
from users.models import User


class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if type(obj) == User:
            return obj == request.user

        return False
