from rest_framework import permissions
from django.contrib.auth.models import User


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        isself = False
        # can be used for Person or User model
        if isinstance(obj, User):
            isself = request.user == obj
        else:
            isself = request.user == obj.user.user
        return request.user.is_staff or isself


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS
