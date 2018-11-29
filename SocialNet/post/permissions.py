from rest_framework import permissions
from post.models import Post
from users.models import User


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if type(obj) == Post:
            return obj.user == request.user

        return False


class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if type(obj) == User:
            return obj == request.user

        return False
