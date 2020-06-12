# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.test import RequestFactory
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, RequestsClient, force_authenticate
from .views import EntityViewSet, UserViewSet, AffiliationViewSet, EntityGenericMaterialViewSet, EntitySpecificMaterialInstanceViewSet, EntitySpecificMaterialViewSet
from .models import *
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core import serializers
import json
from collections import OrderedDict 

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    
    def test_add_manager(self):
        """
        Test de l'ajout d'un manager par un admin
        """
        data = { 'managers' : [self.manager2.pk]}
        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cant_update_entity(self):
        """
        Vérification qu'un utilisateur non manager ne peut modifier une entité
        """
        data = { 'name' : 'nouvelle entité'}
        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.manager2)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_not_add_entity(self):
        """
        Vérification qu'un utilisateur non manager ne peut modifier une entité
        """
        data =  { 'name' : 'Ginova', 'description' : ' Une plateforme en libre accès pour expérimenter', 'contact': 'alain-di-donato@grenoble-inp.fr' } 
        view = EntityViewSet.as_view(actions={'post': 'create'}) 
        request = self.apiFactory.post(reverse('entity-list'),data)
        force_authenticate(request, user=self.manager1)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_add_manager(self):
        """
        Vérification qu'un manager d'une entité peut rajouter un manager
        """
        data =  { 'managers' : [1, 2] } 
        view = EntityViewSet.as_view(actions={'patch': 'partial_update'}) 
        request = self.apiFactory.patch(reverse('entity-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.manager1)
        response = view(request, pk=self.lig_entity.pk)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        managers_lig_obj = self.lig_entity.managers.all()
        list_result = [entry for entry in managers_lig_obj]
        print(list_result)
        self.assertEqual(list_result,[self.manager1, self.manager2])


class UsersTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        self.user = get_user_model().objects.create(username='etudiant1', first_name='etudiant1', email='etudiant@gem-univ-grenoble.fr', password='etudiant1')
        self.user2 = get_user_model().objects.create(username='ensiinfo1', first_name='michel', email='support@ensimag-info.fr', password='matriochka')
        self.affiliation2 = Affiliation.objects.create(name="Grenoble INP", type="Ecole")       
        self.user2.affiliations.add(self.affiliation2)
        self.user2.save()
        self.affiliation = Affiliation.objects.create(name='cnrs', type='Recherche' )
        self.view = UserViewSet.as_view(actions={'patch': 'partial_update'}) 
        self.rgpd_accept_date = datetime.date(2020,6,24)
        self.lig_entity = Entity.objects.create(name = 'LIG', description = 'Laboratoire Informatique de Grenoble', contact='contact-lig@univ-grenoble-alpes.fr') 
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')

    def test_update_self_affiliations(self):
        data = { 'affiliations' : [self.affiliation.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
         
    def test_not_update_user_affiliation(self):
        """
        Test de la protection de l'affiliation d'un autre utilisateur
        """
        data = { 'affiliations' : [self.affiliation2.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.user2)
        response = self.view(request, pk=self.user.id)
        print(self.user.id)
        print(request)
        response.render()
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_rgpd_acceptance_input(self):
        """
        Test du format de la date envoyée
        """
        data = { 'rgpd_accept' : 'True' }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
      
   

class AffiliationsTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.affiliation = Affiliation.objects.create(name='Grenoble INP', type='Ecole')
        self.user =  get_user_model().objects.create(username="max", first_name="max", email='max@univ-grenoble.fr', password='1ngF@b')
   
    def test_affiliation_add(self):
        data = { 'name': 'CNRS', 'type': 'Recherche' }
        view = AffiliationViewSet.as_view(actions={'post': 'create'})
        request = self.apiFactory.post(reverse('affiliation-list'), data)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_affiliation_update(self):
        data = { 'name' : 'UGA' }
        view = AffiliationViewSet.as_view(actions={'patch': 'partial_update'})
        request = self.apiFactory.patch(reverse('affiliation-detail', args=(1, 'pk')), data)
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_affiliation(self):
        data = { 'name' : 'Grenoble INP' }
        view = AffiliationViewSet.as_view(actions={'patch': 'partial_update'})
        request = self.apiFactory.patch(reverse('affiliation-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.user.pk)
        response.render()
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_cant_add_affiliation(self):
        data = { 'name' : 'Inria Grenoble', 'type':'Recherche' }
        view = AffiliationViewSet.as_view(actions={'post': 'create'})
        request = self.apiFactory.post(reverse('affiliation-list'),data)
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class GenericMaterialsTests(APITestCase):

    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.manager2 = get_user_model().objects.create(username="malik", first_name="manager2",email="malik-fabmstic@univ-grenoble-alpes.fr")
        
        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1')
        self.entity = Entity.objects.create(name="ENSAG", description="Ecole Architecture Enseignement Sup",contact="contact@grenoble.archi.fr")
        self.entity.managers.add(self.manager1)
        self.entity.save()
        self.materials_generic = GenericMaterial.objects.create(name="Module RF433,",ref_int="MHZRF433",ref_man="SparkFunMZ433",localisation="FabMSTIC",description="Module radio 433MHZ",quantity="20",entity=self.entity)
        self.client = APIClient()

    def test_view_material(self):
        """
        Test de l'accès bloqué à la liste de matériels pour un utilisateur sans droits
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('genericmaterials-list', kwargs={'entity_pk': 1}))
        response.render()
        # OK 
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_modify_material(self):
        """
        Test de la modification d'un équipement par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = {'name':'Série SC-1608'}
        response = self.client.patch(reverse('genericmaterials-detail', kwargs={'entity_pk':1, 'pk' : 1}), data)
        response.render()
        # OK 
        self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_add_material(self):
        """
        Test de l'ajout d'un équipement par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'FabMSTIC', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire','quantity':'5', 'entity': 1}
        response = self.client.post(reverse('genericmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)

    def test_not_add_material(self):
        self.client.force_authenticate(user=self.user)
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'FabMSTIC', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire','quantity':'5', 'entity': 1}
        response = self.client.post(reverse('genericmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_not_update_material(self):
        self.client.force_authenticate(user=self.manager2)
        data = {'name':'Ensimag'}
        response = self.client.patch(reverse('genericmaterials-detail', kwargs={'pk': 1, 'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

class SpecificMaterialsTests(APITestCase):
    
    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.manager2 = get_user_model().objects.create(username="malik", first_name="manager2",email="malik-fabmstic@univ-grenoble-alpes.fr")
        
        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1')
        self.entity = Entity.objects.create(name="ENSAG", description="Ecole Architecture Enseignement Sup",contact="contact@grenoble.archi.fr")
        self.entity.managers.add(self.manager1)
        self.entity.save()
        self.entity2 = Entity.objects.create(name="Phelma", description="Ecole Ingénieurs Electronique / Physique",contact="contact-phelma@grenoble-inp.fr")
        self.materials_specific = SpecificMaterial.objects.create(name="Zybo ARM/FPGA SoC",ref_int="410-279-RET-PHELMA1",ref_man="410-279-RET",localisation="Etagere 2 - box 4",description="Plateforme programmable FPGA",entity=self.entity)
        self.materials_specific_instance = SpecificMaterialInstance.objects.create(model=self.materials_specific, name="carte ARM/FPGA Soc 1", serial_num="002234", description='instance carte FPGA Phelma' )
        self.client = APIClient()

    def test_add_material(self):
        """
        Test de l'ajout d'un équipement spécifique par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = serializers.serialize('json', [ self.materials_specific, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':1}), material)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)

    def test_not_add_material(self):
        self.client.force_authenticate(user=self.manager2)
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'armoire box électronique, 3eme etage - deuxieme tiroir ', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire', 'entity': 1}
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_not_update_material(self):
        self.client.force_authenticate(user=self.manager2)
        data = {'name':'Tablette ASUS'}
        response = self.client.patch(reverse('specificmaterials-detail', kwargs={'pk': 1, 'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_add_instance_material(self):
        """
        Test de l'ajout d'une instance équipement spécifique par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = serializers.serialize('json', [ self.materials_specific_instance, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk }), material)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    
    def test_not_add_instance_material(self):
        """
        Test de la protection d'ajout d'une instance de matériel spécifique par un utilisateur non manager
        """
        self.client.force_authenticate(user=self.manager2)
        data = serializers.serialize('json', [ self.materials_specific_instance, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk }), material)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_not_update_instance_material(self):
        """
        Test de la protection d'ajout d'une instance de matériel spécifique par un utilisateur non manager
        """
        self.client.force_authenticate(user=self.manager2)
        data = {'name': 'Xtion PRO LIVE'}
        response = self.client.patch(reverse('instances-detail', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk, 'pk': self.materials_specific_instance.pk }), data)
        response.render()
        # OK
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

class LoanMaterialsTests(APITestCase):

    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1')
        self.entity = Entity.objects.create(name="ENSAG", description="Ecole Architecture Enseignement Sup",contact="contact@grenoble.archi.fr")
        self.entity.managers.add(self.manager1)
        self.entity.save()
        self.materials_specific = SpecificMaterial.objects.create(name="Zybo ARM/FPGA SoC",ref_int="410-279-RET-PHELMA1",ref_man="410-279-RET",localisation="Etagere 2 - box 4",description="Plateforme programmable FPGA",entity=self.entity)
        self.materials_specific_instance = SpecificMaterialInstance.objects.create(model=self.materials_specific, name="carte ARM/FPGA Soc 1", serial_num="002234", description='instance carte FPGA Phelma' )
        self.materials_generic = GenericMaterial.objects.create(name="Module RF433,",ref_int="MHZRF433",ref_man="SparkFunMZ433",localisation="FabMSTIC",description="Module radio 433MHZ",quantity="20",entity=self.entity)
        self.materials_specific2 = SpecificMaterial.objects.create(name="Epson projector EBS31 RM1250,",ref_int="EBS31-RM1250_ensag",ref_man="EBS31-RM1250",localisation="perForm - salle matériels video - 1er etage",description="Besoin d'un adaptateur screenbeam pour fonctionner",entity=self.entity)        
        self.materials_specific_instance2 = SpecificMaterialInstance.objects.create(model=self.materials_specific2, name="Epson projector EBS31 RM1250", serial_num="002234", description='instance Epson projector EBS31 RM1250 Ensag' )
        self.loan = Loan.objects.create(status=2, checkout_date = datetime.date(2020,6,8), user=self.user,entity=self.entity, due_date=datetime.date(2020,6,24), return_date=datetime.date(2020,6,24), comments='demande de prêt cours arts visuel')
        self.loan.specific_materials.add(self.materials_specific_instance)
        self.loan.save()
      
        self.entity2 = Entity.objects.create(name="UGA", description="Univ Grenoble Alpes",contact="contact@univ-grenoble.alpes.fr")
        self.entity2.managers.add(self.user)
        self.entity2.save()
        self.loan_manager = Loan.objects.create(status=2, checkout_date = datetime.date(2020,10,8), user=self.manager1,entity=self.entity, due_date=datetime.date(2020,10,24), return_date=datetime.date(2020,10,24), comments='demande de prêt tablettes info')
        self.loan_manager.specific_materials.add(self.materials_specific_instance2)
        self.loan_manager.save()
        self.loan_user = Loan.objects.create(status=2, checkout_date = datetime.date(2020,6,8), user=self.user,entity=self.entity, due_date=datetime.date(2020,7,24), return_date=datetime.date(2020,8,24), comments='demande de prêt tablettes info', parent=self.loan)
        self.loan_user.specific_materials.add(self.materials_specific_instance)
        self.loan_user.save()
        self.client = APIClient()
    
    def test_return_date(self):
        """
           date de retour et date de rendu doivent être après la date de sortie
        """   
        data = {"status" : 3, "checkout_date" : datetime.date(2020,10,8), "user" : self.user.pk , "entity" : 1, "due_date" : datetime.date(2020,6,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': 1}), data)
        response.render()
        self.assertEquals(response.status_code, 400)
        data = {"status" : 3, "checkout_date" : datetime.date(2020,10,8), "user" : self.user.pk , "entity" : 1, "due_date" : datetime.date(2020,10,18), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': 1}), data)
        response.render()
        self.assertEquals(response.status_code, 400)

    def test_entity_loan(self):
        """
            tous les matériels rattachés à un prêt doivent appartenir à l'entité rattaché à ce prêt
        """
        self.client.force_authenticate(user=self.manager1)
        response = self.client.get(reverse('specificmaterials-list', kwargs={'entity_pk': self.entity.pk}), format='json')
        response.render()
       
        try:
            data = serializers.serialize('json', [ self.materials_specific, ])
            struct = json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.exception('Error when parsing JSON, raw data was ' + str(raw_data))
            raise ExternalAPIException('Unable to do my work! Invalid JSON data returned.')
        
        for key, value in enumerate(struct):
            if not 'instances' in value['fields']:
                self.assertEquals(value['fields']['entity'], self.entity.pk)

    def test_create_loan_status(self):
        """
            un utilisateur peut uniquement créer des prêts avec le status requested
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,5,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,6,9), "return_date" : datetime.date(2020,6,5), "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEquals(response.data['status'], 2)


    def test_update_loan_status(self):
        """
            un utilisateur peut uniquement modifier des prêts avec le status pending
        """
        data = {"status" : 1, "checkout_date" : datetime.date(2020,10,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,11,9), "return_date" : datetime.date(2020,11,12), "comments" : 'modification pret 1', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk}),data)
        response.render()
        self.assertEquals(response.data['status'], 1)

    def test_indem_user_loan(self):
       
        """
            un utilisateur ne peut créer de prêts pour un autre utilisateur
        """
        data = {"status" : 3, "checkout_date" : datetime.date(2020,6,8), "user" : self.manager1.pk , "entity" : 1, "due_date" : datetime.date(2020,6,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEquals(response.data['user'], self.user.pk)

        """
            un utilisateur ne peut modifier un prêt pour un autre utilisateur
        """
        data = {"status" : 1, "checkout_date" : datetime.date(2020,6,8), "user" : self.manager1.pk , "entity" : 1, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data, format='json')
        response.render()
        self.assertEquals(response.data['user'], self.user.pk)

    def test_manager_manage_loan(self):
        """
            le manager d'une entité peut créer un prêt rattaché à cette entité pour une autre personne
        """  
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data, format='json')
        response.render()
        self.assertEquals(response.data['user'], self.user.pk)

    def test_own_user_loans(self):
        """
            un utilisateur ne peut voir uniquement les prêts qui lui sont rattachés
        """  
       
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('loan-list'), format='json')
        response.render()
        self.assertEquals(len(response.data), 1)
        
    def test_own_user_loans(self):
        """
            le manager d'une entité peut crée/modifier/supprimer les prêts ratachés à son entité
        """  
      
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data, format='json')
        response.render()
        self.assertEquals(response.status_code,status.HTTP_200_OK)

        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    
    def test_specific_material_instance(self):
        """
            une intance de matériel spécifique ne peut pas appartenir à deux prêts
            qui se chevauche (checkout_date1 < checkout_date2 < return_date1 et vice
            versa)
        """
  
        data = {"status" : 1, "checkout_date" : datetime.date(2020,5,22), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,10,18), "return_date" : datetime.date(2020,8,28), "comments" : 'prêt en cours TP embarqué ens3', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data)
        response.render()
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)

        data = {"status" : 1, "checkout_date" : datetime.date(2020,8,10), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,8,20), "return_date" : datetime.date(2020,9,1), "comments" : 'demande de prêt matériel embarqué', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data)
        response.render()
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_child_loan(self):
        """
            Seul un manager peut créer un prêt enfant d'un autre pret
            Vérification de la même entité pour la copie du prêt
        """
        parent = self.loan_user.pk
        data = {"status" : 1, "checkout_date" : datetime.date(2020,8,30), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,9,10), "return_date" : datetime.date(2020,9,15), "comments" : 'prolongation du prêt de tablettes, ajout de retroprojecteur', 'specific_materials': [self.materials_specific_instance.pk, self.materials_specific_instance2.pk], 'generic_materials': [], 'parent': self.loan_user.pk }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('loan-list'), data)
        response.render()
        self.assertTrue(response.data['parent'])
        self.assertEquals(response.data['parent'], self.loan_user.pk)  

    def test_child_loan_not_created(self):    
        parent = self.loan.pk
        data = {"status" : 1, "checkout_date" : datetime.date(2020,8,30), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,9,10), "return_date" : datetime.date(2020,9,15), "comments" : 'prolongation du prêt de tablettes, ajout de retroprojecteur', 'specific_materials': [self.materials_specific_instance.pk, self.materials_specific_instance2.pk], 'generic_materials': [], 'parent': self.loan_user.pk }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data)
        response.render()
        self.assertIsNone(response.data['parent'])
    
    def test_protected_loan_return_date(self):    
        data = {"status" : 1, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,26), "comments" : 'modification date retour', 'specific_materials': [], 'generic_materials': []}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail',  kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEquals(response.data['return_date'], "2020-08-24")
    
    def test_protected_loan_parent(self):    
        data = {"status" : 1, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,26), "comments" : 'modification date retour', 'specific_materials': [], 'generic_materials': [],  'parent': self.loan_manager.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail',  kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEquals(response.data['parent'], self.loan.pk)

    def test_protected_loan_user(self): 
        """
            un utilisateur ne peut modifier les champs, parent, return_date et
            user (transfert vers un autre utilisateur)
        """
        print('====')
        print(self.loan_user.user.pk)
        # test protection utilisateur
        data = {"status" : 1, "checkout_date" : datetime.date(2020,6,8), "user" : 1 , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,24), "comments" : 'prolongation du prêt de tablettes, ajout de retroprojecteur', 'specific_materials': [], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        print('======')
        print(response.data)
        print('-----')
        print(self.manager1.pk)
        print(self.user.pk)
        self.assertEquals(response.data['user'], 2)
      