# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAdminUser
from rest_framework import viewsets, mixins, status
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Entity, Affiliation, SpecificMaterial, SpecificMaterialInstance, GenericMaterial

from .serializers import *   
from .permissions import EntityPermission, IsManager, IsAdminOrIsSelf, IsAdminOrReadOnly 
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

        Only need first_name, ViewSetMixinlast_name and email

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
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        instance = UserSerializer(request.user, context={'request': request})
        return Response({"user": instance.data})

class EntityViewSet(viewsets.ModelViewSet):
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
        return Response(dict((x, y) for x, y in Affiliation.TYPE_AFFILIATION), status=status.HTTP_200_OK)

class EntityMaterialMixin:
    def get_queryset(self):
        entity = get_object_or_404(Entity.objects, pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        return self.queryset.filter(entity=entity)
    def create(self, request, *args, **kwargs):
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        request.data.update({'entity':self.kwargs['entity_pk']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EntityGenericMaterialViewSet(viewsets.ModelViewSet, EntityMaterialMixin):
    queryset = GenericMaterial.objects.all()
    permission_classes = (IsManager,)
    serializer_class = GenericMaterialSerializer

class EntitySpecificMaterialViewSet(EntityMaterialMixin, viewsets.ModelViewSet):
    queryset = SpecificMaterial.objects.all()
    permission_classes = (IsManager,)
    serializer_class = SpecificMaterialSerializer

class EntitySpecificMaterialInstanceViewSet(viewsets.ModelViewSet):
    queryset = SpecificMaterialInstance.objects.all()
    permission_classes = (IsManager,)
    serializer_class = SpecificMaterialInstanceSerializer
    def get_queryset(self):
        print(self.kwargs)
        entity = get_object_or_404(Entity.objects, pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        if not entity.specificmaterials.filter(id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied("This material does not belong to your entity")
        return self.queryset.filter(model__entity=entity, model=self.kwargs['specificmaterial_pk'])

    def create(self, request, *args, **kwargs):
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and not self.request.user in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        if not entity.specificmaterials.filter(id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied("This material does not belong to your entity")
        request.data.update({'model':self.kwargs['specificmaterial_pk']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



