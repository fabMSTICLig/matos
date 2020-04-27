from rest_framework import permissions
from .models import Entity


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        isself = request.user == obj
        return request.user.is_staff or isself

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.method)
        ismanager = False
        if isinstance(obj, Entity):
            ismanager = request.user in obj.managers.all()
        return request.user.is_staff or ismanager and request.method in ['PUT','PATCH'] or request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or (request.user.is_authenticated and request.method != "POST"))
