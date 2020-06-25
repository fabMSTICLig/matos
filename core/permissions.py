from rest_framework import permissions
from .models import Entity, SpecificMaterial,SpecificMaterialInstance, GenericMaterial, Loan


class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Permission checking if user is admin or if the object belongs to the current user.
    The object field must be 'user'
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        isself = request.user == obj
        return request.user.is_staff or isself

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS

class EntityPermission(permissions.BasePermission):
    """
    Special permission for an entity
    User must be anthentificated
    GET all user
    PUT PATCH managers on the entity
    POST and DELETE only admin
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        ismanager = False
        if isinstance(obj, Entity):
            ismanager = request.user in obj.managers.all()
        return ismanager and request.method in ['PUT','PATCH'] or request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or (request.user.is_authenticated and request.method != "POST"))

class RGPDAccept(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rgpd_accept is not None

class IsManagerOf(permissions.BasePermission):
    """
    Permission used for material
    User must be anthentificated
    GET all user
    PUT PATCH POST DELETE managers on the entity or admin
    """

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

class IsManagerCreateOrReadOnly(permissions.BasePermission):
    """
    Permission readonly or create for entity manager, used for tag
    User must be anthentificated
    LIST GET authenticated
    POST manager of at least one entity
    DELETE PUT PATCH Admin
    """
    def has_permission(self, request, view):
        return (request.user and
            (request.user.is_staff or
            request.method in permissions.SAFE_METHODS or
           request.user.is_authenticated and request.user.entities.all().count()>0 and request.method == "POST"))

class LoanPermission(permissions.BasePermission):
    """
    Special permission for a loan
    User must be anthentificated
    GET PUT PATCH owner
    POST autenticated user
    DELETE manager of entity
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        ismanager = False
        if isinstance(obj, Loan):
            ismanager = request.user in obj.entity.managers.all()
            if request.user == obj.user:
                safeDestroy = (request.method == 'DELETE' and not ismanager) and obj.status == int(Loan.Status.REQUESTED) 
        return ismanager or safeDestroy or (request.user == obj.user and request.method != 'DELETE') 

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
