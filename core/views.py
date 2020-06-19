# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAdminUser
from rest_framework import viewsets, mixins, status
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.decorators import action


from .models import Entity, Affiliation,Tag, SpecificMaterial, SpecificMaterialInstance, GenericMaterial, Loan, LoanGenericItem


from .serializers import *
from .permissions import EntityPermission, IsManagerCreateOrReadOnly, IsManagerOf, IsAdminOrIsSelf, IsAdminOrReadOnly, LoanPermission
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')

    def get_serializer_class(self):
        """
        Non admin user cannot see private user attribute for privacy reason
        """
        if self.action == "list" and not self.request.user.is_staff:
            return UserPublicSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'retrieve', 'set_password']:
            permission_classes = [IsAdminOrIsSelf, IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['put'], detail=True, serializer_class=PasswordSerializer)
    def set_password(self, request, pk):
        """
        Special endpoint to change password
        """
        serializer = PasswordSerializer(data=request.data)
        user = get_user_model().objects.get(pk=pk)
        # only an admin or the own user can change the password
        if request.user.is_staff or user == request.user:
            if serializer.is_valid():
                if not user.check_password(serializer.data.get('old_password')):
                    return Response({'old_password': ['Wrong password.']},
                                    status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request,user)
                return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=NewUserSerializer)
    def create_user(self, request):
        """
        Special end point for creating user

        Only need first_name, last_name and email

        Generate a unique usermane and a password
        """
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            firstname = serializer.data.get('first_name')
            lastname = serializer.data.get('last_name')
            email = serializer.data.get('email')
            username = (lastname[:7]+firstname[0]).lower()
            count = 2
            while(get_user_model().objects.filter(username=username).exists()):
                username = (lastname[:7]+firstname[0]).lower()+str(count)
                count = count+1
            password = username[::-1]
            user = get_user_model().objects.create_user(username, email, password)
            user.last_name = lastname
            user.first_name = firstname
            user.save()
            serialized_class = UserSerializer(user)
            return Response(serialized_class.data, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class SelfView(APIView):
    """
    Endpoint to see personals informations/profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        instance = UserSerializer(request.user, context={'request': request})
        return Response({"user": instance.data})

class EntityViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the entities
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = (EntityPermission,)

class AffiliationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows affiliations to be viewed or edited.
    """
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=False)
    def types(self, request):
        """
        Return the affiliation types
        """
        return Response(dict((x, y) for x, y in Affiliation.TYPE_AFFILIATION), status=status.HTTP_200_OK)

class TagViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the material tags
    """
    queryset = Tag.objects.all()
    permission_classes = (IsManagerCreateOrReadOnly,)
    serializer_class = TagSerializer

    @action(methods=['delete'], detail=False)
    def delete_unused(self, request):
        """
        Special end point for deleteing unused tag
        return list of ids of deleted tags
        """
        if request.user.is_staff:
            unusedtags = Tag.objects.filter(genericmaterials=None, specificmaterials=None)
            ids = list(unusedtags.values_list('id', flat=True))
            unusedtags.delete()
            return Response(ids, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()



class EntityMaterialMixin:
    """
    Mixin used for common methods beetween Specific and Generic material
    """
    def get_queryset(self):
        """
        Limit material to a specific entity using the nested route system
        Check if the current user is an admin or if he is a manager of the entity
        """
        entity = get_object_or_404(Entity.objects, pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        return self.queryset.filter(entity=entity)
    def create(self, request, *args, **kwargs):
        """
        Check if the current user is an admin or if he is a manager of the entity
        Overide the entity props of the material to the one in the url
        """
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        request.data.update({'entity':self.kwargs['entity_pk']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        """
        Avoid the entity prop to be updated (transfert of material beetween entities)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data.update({'entity':instance.entity.id})
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class EntityGenericMaterialViewSet(EntityMaterialMixin, viewsets.ModelViewSet):
    """
    Manager endpoints for generic material
    Use nested router params
    """
    queryset = GenericMaterial.objects.all()
    permission_classes = (IsManagerOf,)
    serializer_class = GenericMaterialSerializer

class GenericMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoints for generic material
    """
    queryset = GenericMaterial.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GenericMaterialPublicSerializer

class EntitySpecificMaterialViewSet(EntityMaterialMixin, viewsets.ModelViewSet):
    """
    Endpoints for specific material
    Use nested router params
    """
    queryset = SpecificMaterial.objects.all()
    permission_classes = (IsManagerOf,)
    serializer_class = SpecificMaterialSerializer

class SpecificMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoints for specific material
    """
    queryset = SpecificMaterial.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SpecificMaterialPublicSerializer


class EntitySpecificMaterialInstanceViewSet(viewsets.ModelViewSet):
    """
    Endpoints for instance of specific material
    Use nested router params
    """
    queryset = SpecificMaterialInstance.objects.all()
    permission_classes = (IsManagerOf,)
    serializer_class = SpecificMaterialInstanceSerializer
    def get_queryset(self):
        """
        Filter the queryset using entity_pk and specificmaterial_pk of the nested router
        Check if the current user is an admin or if he is a manager of the entity owning the material
        Check if the instance belongs to the specific material id in the nested router params
        """
        entity = get_object_or_404(Entity.objects, pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        if not entity.specificmaterials.filter(id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied("This material does not belong to your entity")
        return self.queryset.filter(model__entity=entity, model=self.kwargs['specificmaterial_pk'])

    def create(self, request, *args, **kwargs):
        """
        Check if the current user is an admin or if he is a manager of the entity owning the material
        Check if the instance belongs to the specific material id in the nested router params
        """
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        if not entity.specificmaterials.filter(id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied("This material does not belong to your entity")
        request.data.update({'model':int(self.kwargs['specificmaterial_pk'])})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Avoid the model prop to be updated (transfert of instance beetween material)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data.update({'model':instance.model.id})
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class SpecificMaterialInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoints for specific material instance
    """
    queryset = SpecificMaterialInstance.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SpecificMaterialInstanceSerializer
    def get_queryset(self):
        return self.queryset.filter(model=self.kwargs['specificmaterial_pk'])



class LoanViewSet(viewsets.ModelViewSet):
    """
    Endpoints for loans
    """
    queryset = Loan.objects.all()
    permission_classes = (LoanPermission,)
    serializer_class = LoanSerializer

    def get_queryset(self):
        """
        """
        if(self.request.user.is_staff):
            return self.queryset.all()
        return self.queryset.filter(Q(user=self.request.user) | Q(entity__managers__in = [self.request.user])).distinct()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(not request.user.is_staff and request.user not in serializer.validated_data['entity'].managers.all()):
            if serializer.validated_data['user']!=request.user:
                serializer.validated_data['user']=request.user
            if serializer.validated_data['status'] != Loan.Status.REQUESTED:
                serializer.validated_data['status']=Loan.Status.REQUESTED
            if serializer.validated_data['return_date']:
                serializer.validated_data['return_date']=None
            serializer.validated_data['parent']=None
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(not request.user.is_staff and request.user not in serializer.validated_data['entity'].managers.all()):
            if (serializer.validated_data['status'] != int(Loan.Status.PENDING) and serializer.validated_data['status'] != int(Loan.Status.REQUESTED)) or instance.status == Loan.Status.ACCEPTED :
                raise PermissionDenied("Vous ne pouvez pas modifier un prêt qui a été accepté ou refusé")
            request.data.update({'user':instance.user.id})
            request.data.update({'return_date':instance.return_date})
            request.data.update({'parent':instance.parent.id if instance.parent else instance.parent})     
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def status(self, request):
        """
        Return the affiliation types
        """
        return Response(dict((x, y) for x, y in Loan.Status.choices), status=status.HTTP_200_OK)



