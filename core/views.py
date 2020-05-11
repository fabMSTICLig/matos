# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAdminUser
from rest_framework import viewsets, mixins, status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Entity, Affiliation
from .serializers import *   
from .permissions import *
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
    permission_classes = (IsManagerOrReadOnly,)

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
