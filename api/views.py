# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, get_user
from django.shortcuts import render
from django.views.generic.edit import CreateView
from rest_framework import viewsets, serializers, status, generics, mixins, authentication, permissions
from rest_framework.decorators import api_view,permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Product , Location ,Family ,Transaction, Organization, Person
from .serializers import *   
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.http import JsonResponse
from rest_framework.permissions import *
from api.forms import  OrganizationForm
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django_cas_ng import views as baseviews
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from .permissions import *

@api_view(["GET"])
def index(request):
    if request.user.is_authenticated:
        return HttpResponse('<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p>You logged in as <strong>%s</strong>.</p><p><a href="/accounts/logout">Logout</a></p>' % request.user)
    else:
        return HttpResponse('<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p><a href="/accounts/login">Login</a></p>')


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def signup_success(request):
    data = "inscription utilisateur réussie"
    return Response(data, status=HTTP_200_OK)


class PersonView(FormView):
    template_name = 'person.html'
    ##form_class = PersonForm
    success_url = '/signup-success'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class get_users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class OrganizationView(FormView):
    template_name = 'organization.html'
    form_class = OrganizationForm
    success_url = '/signup-success'

    def form_valid(self, form):
        print("organization process adding")
        form.save()
        return super().form_valid(form)



class productListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

class productInstanceListView(viewsets.ModelViewSet):
    queryset = ProductInstance.objects.all()
    serializer_class = ProductInstanceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
class organizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, format=None):
        organization = self.get_organization(pk)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        print("put")
        permission_classes = (IsManager,)
        user=get_user(request)
        print(user.has_perm('manage_entity'))
        return self.update(request, *args,**kwargs) 
    
        #Helper method to get a person
    def get_organization(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404
    
    def patch(self, request, pk):
        instance_object = self.get_object(pk)
        print(request)
        print('patch')
        permission_classes = (IsManager,)

        serializer = OrganizationSerializer(instance_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'code':201, 'data':serializer.data})
        return JsonResponse({'code':400, 'data':"wrong parameters"})
    
   

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

class location_list(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class location_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Location.objects.all()
    serializer_class =  LocationSerializer    

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class transaction_list(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        

class transaction_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class =  TransactionSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args,**kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args,**kwargs) 

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)  


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

