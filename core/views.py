# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.auth import authenticate, get_user
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, View
from rest_framework import viewsets, serializers, status, filters,  generics, mixins, authentication, permissions
from rest_framework.decorators import api_view,permission_classes, action, renderer_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Entity, Profile, Affiliation
from .serializers import *   
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.http import JsonResponse
from rest_framework.permissions import *
from django.views.generic.list import ListView
from django_cas_ng import views as baseviews
from django.http import HttpResponseRedirect, HttpResponse , QueryDict, Http404
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from .permissions import *
from rest_framework.renderers import JSONRenderer

@api_view(["GET"])
def index(request):
    if request.user.is_authenticated:
        return HttpResponse('<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p>You logged in as <strong>%s</strong>.</p><p><a href="/accounts/logout">Logout</a></p>' % request.user)
    else:
        return HttpResponse('<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p><a href="/accounts/login">Login</a></p>')



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
            permission_classes = [IsAdminOrIsSelf]
        elif self.action in ['update', 'partial_update', 'retrieve', 'set_password']:
            permission_classes = [IsAdminOrIsSelf, IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

      
        #Helper method to get a person
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        print(user.id)
        print('## patch user ##')
    
        permission_classes = (IsAuthenticatedOrReadOnly,)
        serializer = UserSerializer(user, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            if(isinstance(request.data, QueryDict)):
                data = request.data.dict()
            else:
                data = dict(request.data)

          

            print("## profile ##")
            username = data['username']
            firstname = data['first_name']
            lastname = data['last_name']
            acceptance = data['profile']['acceptance']
            affiliations = data['profile']['affiliations']

            profile = Profile.objects.get(user=user)
            if(acceptance == True):
                profile.acceptance = datetime.datetime.now(datetime.timezone.utc).date()
            else:
                profile.acceptance=None

            profile.affiliations.clear()
            profile.email = data['profile']['email']

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                profile.affiliations.add(affiliation_obj)

            profile.save()          
            print(profile.acceptance)
            user.profile = profile
            user.username = username
            user.first_name = firstname
            user.last_name = lastname

            user.save()
           
            return JsonResponse({'code':201, 'data':serializer.data})
        print(serializer.errors)

        return JsonResponse({'code':400, 'data':"wrong parameters"})

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



class get_users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class entityManagedListView(generics.ListCreateAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

   
    def list(self, request):
        user = request.user
        print('## user')
        print(user.id)
        queryset = Entity.objects.filter(managed__in=[user.id])
        serializer = EntitySerializer(queryset, many=True)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

class entityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = (IsAdminOrIsSelf)

    #Helper method to get a person
    def get_entity(self, pk):
        try:
            return Entity.objects.get(pk=pk)
        except Entity.DoesNotExist:
            raise Http404

    def get_permissions(self):
        print(self.action)
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'delete']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update']:
            permission_classes = [IsManager,IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
            
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """
        Overload update method in order to limit standard user actions
        """
        if(isinstance(request.data, QueryDict)):
            data = request.data.dict()
        else:
            data = dict(request.data)
        # Auto complete if normal user or admin for own usage by removing user member
        if(not request.user.is_staff or not 'user' in data):
            data['user'] = request.user
            entity = Entity.objects.get(pk=data['id'])
            entity.name = data['name']
            entity.contact = data['contact']
            affiliations = data['affiliations']
            managers = data["managed"]
            print(entity.name)
            print(Entity.objects.filter(name=entity.name))          
            entity.save()
          
            try:
                entity.save() # Could throw exception
            except IntegrityError:
                transaction.rollback()

            entity.affiliations.clear()

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                entity.affiliations.add(affiliation_obj)
            
            entity.save()
            entity.managed.clear()

            for manager in managers :
                print(manager['id'])
                manager_obj = User.objects.get(pk=manager['id'])
                manager_obj.first_name = manager['first_name']
                manager_obj.last_name = manager['last_name']
                manager_obj.externe = manager['externe']
                manager_obj.is_staff = manager['is_staff']
                manager_obj.username = manager['username']

                print(manager_obj.username)
                manager_obj.save()
                entity.managed.add(manager_obj)

        entity.save()
        serialized_class = EntitySerializer(entity)
        print(serialized_class.data)
        return Response(serialized_class.data, status=status.HTTP_200_OK)

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
            entity = Entity()
            entity.name = data['name']
            entity.contact = data['contact']
            affiliations = data['affiliations']
            print(entity.name)
            print(Entity.objects.filter(name=entity.name))
            try:
                entity_existing = Entity.objects.get(name=entity.name)
                print("existing orga")
                print(entity_existing)
                if entity_existing :
                    return Response("entity already registered with same name", status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
  
            entity.save()
          
            try:
                entity.save() # Could throw exception
            except IntegrityError:
                transaction.rollback()

            entity.affiliations.clear()

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                entity.affiliations.add(affiliation_obj)
            
            entity.save()
               
        serialized_class = EntitySerializer(entity)
        print(serialized_class.data)
        return Response(serialized_class.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk, format=None):
        print('suppression')
        entity = self.get_entity(pk)
        id=pk
        print(pk)
        entity.delete() 
        return Response({"id" :id}, status=status.HTTP_200_OK)
    
   




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
            permission_classes = (IsAdminOrIsSelf,)
            return PublicAffiliationSerializer
        
        elif self.action in ['update', 'partial_update', 'retrieve', 'create']:
            permission_classes = (IsAdminUser,)
            return AffiliationSerializer

        else:
            print("Affiliation Serializer")
            permission_classes = (IsAdminUser,)
            return AffiliationSerializer

class UserInstanceView(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        print("self api")
        print(request)
        if request.user.is_authenticated:
            instance = UserSerializer(request.user, context={'request': request})
            if request.user.groups.filter(name='manager'):
                return Response({"user": instance.data, "manager":True})
            else:
                return Response({"user": instance.data, "manager":False})
        return Response({"not authorized"})
        #return Response('appel api')

