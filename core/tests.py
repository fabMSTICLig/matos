# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.test import RequestFactory
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, RequestsClient, force_authenticate
from .views import EntityViewSet, UserViewSet, AffiliationViewSet
from .models import *


class EntitiesTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1")
        self.manager2 = get_user_model().objects.create(username="manager2", first_name="manager2")
        #ajout des entités
        self.lig_entity = Entity.objects.create(name = 'LIG', description = 'Laboratoire Informatique de Grenoble', contact='contact-lig@univ-grenoble-alpes.fr') 
        self.ensimag_entity = Entity.objects.create(name = 'ENSIMAG', description = 'Ecole ENSIMAG - Grenoble INP', contact='contact-ensimag@grenoble-inp.fr') 
        self.lig_entity.managers.add(self.manager1)
        self.lig_entity.save()
        #ajout d'un admin
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        
    def test_not_manager_update(self):    
        managers_lig_obj = self.lig_entity.managers.all()
        list_result = [entry for entry in managers_lig_obj]
        self.assertEqual(list_result,[self.manager1])
        self.user = self.manager2

        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        data = { 'name' : "FabMSTIC" }
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        self.assertEqual(response.status_code, 403)

    def test_manager_update(self):
       
        managers_lig_obj = self.lig_entity.managers.all()
        list_result = [entry for entry in managers_lig_obj]
        self.assertEqual(list_result,[self.manager1])
        self.user = self.manager1

        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        data = { 'name' : "FabMSTIC" }
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        self.assertEqual(response.status_code, 200)
   
    def test_add_entity(self):
        """
        Ensure we can create a new entity object.
        """
        data = { 'name' : 'Ginova', 'description' : ' Une plateforme en libre accès pour expérimenter', 'contact': 'alain-di-donato@grenoble-inp.fr' } 
        view = EntityViewSet.as_view(actions= {'post': 'create'})
        request = self.apiFactory.post(reverse('entity-list'),data)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        response.render()
        data = response.data
        self.assertEqual(response.data['name'], 'Ginova')

    def test_delete_entity(self):
        """
        Ensure we can create a new entity object.
        """
        view = EntityViewSet.as_view(actions= {'delete': 'destroy'})
        request = self.apiFactory.delete(reverse('entity-detail', args=(1, 'pk')))
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=1)
        response.render()
        data = response.data
        self.assertEqual(response.status_code, 204)

class UsersTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)
    
    def setUp(self):
        self.apiFactory = self.api_factory()
        self.user = get_user_model().objects.create(username='etudiant1', first_name='etudiant1', email='etudiant@gem-univ-grenoble.fr', password='etudiant1')
        self.affiliation = Affiliation.objects.create(name='cnrs', type='Recherche' )
        self.view = UserViewSet.as_view(actions={'patch': 'partial_update'}) 
        self.rgpd_accept_date = datetime.date(2020,5,24)
        self.lig_entity = Entity.objects.create(name = 'LIG', description = 'Laboratoire Informatique de Grenoble', contact='contact-lig@univ-grenoble-alpes.fr') 
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
    
    def test_update_self_affiliations(self):
        data = { 'affiliations' : [self.affiliation.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEquals(response.status_code, 200)
         
    def test_update_self_affiliations_admin(self):
        data = { 'affiliations' : [self.affiliation.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEquals(response.status_code, 200)
    
    def test_rgpd_acceptance_input(self):
        """
        Test du format de la date envoyée
        """
        data = { 'rgpd_accept' : 'True' }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = self.view(request, pk=self.user.id)
        response.render()
        print(response)
        self.assertEquals(response.status_code,400)

    def test_rgpd_acceptance_date(self):
        """
        Test de la date envoyée au bon format
        """
        data = { 'rgpd_accept' : datetime.date(2020,5,27) }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.user.id)
        response.render()
        print(response)
        self.assertEquals(response.status_code,200)

    def test_add_manager(self):
        """
        Test de l'ajout d'un manager par un admin
        """
        data = { 'managers' : [self.user.pk]}
        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        self.assertEqual(response.status_code, 200)

class AffiliationsTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)
        
    def setUp(self):
        self.apiFactory = self.api_factory()
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.affiliation = Affiliation.objects.create(name='Grenoble INP', type='Ecole')
    
    def test_affiliation_add(self):
        data = { 'name': 'CNRS', 'type': 'Recherche' }
        view = AffiliationViewSet.as_view(actions={'post': 'create'})
        request = self.apiFactory.post(reverse('affiliation-list'), data)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 201)
    
    def test_affiliation_delete(self):
        view = AffiliationViewSet.as_view(actions={'delete': 'destroy'})
        request = self.apiFactory.delete(reverse('affiliation-detail', args=(1, 'pk')))
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 204)

    def test_affiliation_update(self):
        data = { 'name' : 'UGA' }
        view = AffiliationViewSet.as_view(actions={'patch': 'partial_update'})
        request = self.apiFactory.patch(reverse('affiliation-detail', args=(1, 'pk')), data)
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 200)