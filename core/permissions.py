from rest_framework import permissions
from .models import Entity, SpecificMaterial,SpecificMaterialInstance, GenericMaterial


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        isself = request.user == obj
        return request.user.is_staff or isself

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS

class EntityPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        ismanager = False
        if isinstance(obj, Entity):
            ismanager = request.user in obj.managers.all()
        return request.user.is_staff or ismanager and request.method in ['PUT','PATCH'] or request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or (request.user.is_authenticated and request.method != "POST"))

class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        ismanager = False
        if isinstance(obj, SpecificMaterial) or isinstance(obj, GenericMaterial):
            ismanager = request.user in obj.entity.managers.all()
        elif isinstance(obj, SpecificMaterialInstance):
            ismanager = request.user in obj.model.entity.managers.all()
        return ismanager

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
