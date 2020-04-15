# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from .models import Product , Location ,Family ,Transaction, Organization, Profile
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
        print(user)
        print('## patch user ##')
        permission_classes = (IsAuthenticatedOrReadOnly,)

       

        serializer = UserSerializer(user, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            if(isinstance(request.data, QueryDict)):
                data = request.data.dict()
            else:
                data = dict(request.data)

            profile = Profile.objects.get(pk=data['id'])
            print("## profile ##")
            print(data)
            profile.username = data['username']
            profile.firstname = data['firstname']
            profile.lastname = data['username']
            profile.email = data['email']
            profile.acceptance = data['acceptance']
            profile.save()
            user.profile = profile
            user.save()
            print("##user##")
            print(user)
           
            return JsonResponse({'code':201, 'data':serializer.data})
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




class productListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

class productInstanceListView(viewsets.ModelViewSet):
    queryset = ProductInstance.objects.all()
    serializer_class = ProductInstanceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class organizationManagedListView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

   
    def list(self, request):
        user = request.user
        print('## user')
        print(user.id)
        queryset = Organization.objects.filter(managed__in=[user.id])
        serializer = OrganizationSerializer(queryset, many=True)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)



class organizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAdminOrIsSelf)



    def retrieve(self, request, pk=None):
        pass

    #Helper method to get a person
    def get_organization(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404

    def get_permissions(self):
        print(self.action)
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'retrieve','create', 'delete']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
            
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
            organization = Organization.objects.get(pk=data['id'])
            organization.name = data['name']
            organization.contact = data['contact']
            affiliations = data['affiliations']
            managers = data["managed"]
            print(organization.name)
            print(Organization.objects.filter(name=organization.name))          
            organization.save()
          
            try:
                organization.save() # Could throw exception
            except IntegrityError:
                transaction.rollback()

            organization.affiliations.clear()

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                organization.affiliations.add(affiliation_obj)
            
            organization.save()
            organization.managed.clear()

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
                organization.managed.add(manager_obj)

        organization.save()
        serialized_class = OrganizationSerializer(organization)
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
            organization = Organization()
            organization.name = data['name']
            organization.contact = data['contact']
            affiliations = data['affiliations']
            print(organization.name)
            print(Organization.objects.filter(name=organization.name))
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

            organization.affiliations.clear()

            for affiliation in affiliations:
                affiliation_obj = Affiliation.objects.get(pk=affiliation['id'])
                organization.affiliations.add(affiliation_obj)
            
            organization.save()
               
        serialized_class = OrganizationSerializer(organization)
        print(serialized_class.data)
        return Response(serialized_class.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk, format=None):
        print('suppression')
        organization = self.get_organization(pk)
        id=pk
        print(pk)
        organization.delete() 
        return Response({"id" :id}, status=status.HTTP_200_OK)
    
   

class productDetailViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    print('>>>>>')
    def get(self, request, *args, **kwargs):
        print("equipment view")
        data=self.retrieve(request, *args,**kwargs)
        return self.retrieve(request, *args,**kwargs) 
    
    def put(self, request, *args, **kwargs):
        print("equipment view")
        print("mise a jour produit")
        families_data = self.request.data['categories']
        equipment_id = self.request.data['id']
        location_id = self.request.data['location']
        equipment = Product.objects.get(pk=equipment_id)
        equipment.title =  self.request.data['title']
        equipment.description = self.request.data['description']
        equipment.barcode = self.request.data['barcode']
        equipment.location = Location.objects.get(pk=location_id)
        equipment.sku = self.request.data['sku']
        equipment.refUsine = self.request.data['refUsine']
        equipment.categories.clear()
        
        for family in families_data :
            family_obj = Family.objects.get(pk=family['id'])
            equipment.categories.add(family_obj)

        equipment.save() 
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 

class family_list(generics.ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class family_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args,**kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args,**kwargs) 

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)       


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

