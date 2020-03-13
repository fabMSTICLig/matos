from django.shortcuts import render
from rest_framework import viewsets, serializers, status, generics, mixins, authentication, permissions
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import filters
import traceback
import sys
from api.models import Organization, Affiliation
from .permissions import IsAdminOrIsSelf, IsAdminOrReadOnly
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import QueryDict, Http404
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.db import transaction, DatabaseError
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
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
        print(self.action)
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
        user = User.objects.get(pk=pk)
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
            while(User.objects.filter(username=username).exists()):
                username = (lastname[:7]+firstname[0]).lower()+str(count)
                count = count+1
            password = username[::-1]
            user = User.objects.create_user(username, email, password)
            user.last_name = lastname
            user.first_name = firstname
            user.save()
            serialized_class = UserSerializer(user)
            return Response(serialized_class.data, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class AffiliationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """
        Non admin user cannot see private user attribute for privacy reason
        """
        if self.action == "list" and not self.request.user.is_staff:
            return PublicAffiliationSerializer
        else:
            print("Affiliation Serializer")
            return AffiliationSerializer

class SelfView(APIView):
    def get(self, request, format=None):
        print("self api")
        print(request)
        instance = UserSerializer(request.user, context={'request': request})
        return Response({"user": instance.data})
        #return Response('appel api')

class organizationListView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        print(self.action)
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'retrieve', 'set_password']:
            permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Overload create method for auto completing user, date and validated member
        """
        if(isinstance(request.data, QueryDict)):
            data = request.data.dict()
        else:
            data = dict(request.data)
        # Auto complete if normal user or admin for own usage by removing user member
        if(not request.user.is_staff or not 'user' in data):
            data['user'] = request.user
            organization = Organization()
            organization.name = data['name']
            organization.contact = data['contact']
            affiliations = data['affiliations']

            try:
                organization_existing = Organization.objects.get(name=organization.name)
                print("existing orga")
                print(organization_existing)
                if organization_existing :
                      return Response("entity already registered with same name", status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
  
            organization.save()
          
            try:
                organization.save() # Could throw exception
            except IntegrityError:
                transaction.rollback()

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                organization.affiliations.add(affiliation_obj)
            
            organization.save()
            #for manager in managers :
             #   manager_obj = User.objects.get(pk=manager['id'])
              #  organization.manager.add(manager_obj)
        
        serialized_class = OrganizationSerializer(organization)
        headers = self.get_success_headers(serialized_class.data)
        print(serialized_class.data)
        return Response(serialized_class.data, status=status.HTTP_201_CREATED, headers=headers)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 