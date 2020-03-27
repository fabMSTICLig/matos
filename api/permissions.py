from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Person


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        isself = False
        # can be used for Person or User model
        if isinstance(obj, Person):
            isself = request.user == obj.user
        elif isinstance(obj, User):
            isself = request.user == obj
        else:
            isself = request.user == obj.user.user
        return request.user.is_admin or isself


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager or request.method in permissions.SAFE_METHODS

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='manager'):
            return True
        return False
