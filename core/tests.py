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
from django.utils import timezone

class EntitiesTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1")
        self.manager2 = get_user_model().objects.create(username="manager2", first_name="manager2")
        self.manager1.rgpd_accept = timezone.now().date()
        self.manager1.save()
        self.manager2.rgpd_accept = timezone.now().date()
        self.manager2.save()
        #ajout des entités
        self.lig_entity = Entity.objects.create(name = 'LIG', description = 'Laboratoire Informatique de Grenoble', contact='contact-lig@univ-grenoble-alpes.fr')
        self.ensimag_entity = Entity.objects.create(name = 'ENSIMAG', description = 'Ecole ENSIMAG - Grenoble INP', contact='contact-ensimag@grenoble-inp.fr')
        self.lig_entity.managers.add(self.manager1)
        self.lig_entity.save()
        #ajout d'un admin
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.superuser.rgpd_accept = timezone.now().date()
        self.superuser.save()

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
        """
        Verify that manager can update entity
        """
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
        self.assertEqual(list_result,[self.manager1, self.manager2])

    def test_loans_specificmaterial(self):
        """
        Vérification d'accès aux prêts d'un materiel spécifique
        """
        data={"name": "camera viso", "ref_int":"visio-angle-large"}
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':self.lig_entity.pk}),data)
        response.render()
        specificmaterial_pk = response.data['id']

        data={"serial_num": "cam1", "name":"instance1"}
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':self.lig_entity.pk,'specificmaterial_pk':specificmaterial_pk}),data)
        response.render()
        instance_pk =  response.data['id']

        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,25), "user" : self.manager1.pk , "entity" : self.lig_entity.pk, "due_date" : datetime.date(2020,7,25), "return_date" : datetime.date(2020,7,25), "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [instance_pk], 'generic_materials': []}
        response = self.client.post(reverse('loan-list'),data)
        response.render()

        response = self.client.get(reverse('loan-list'), {'smi':instance_pk})
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)





class UsersTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        self.user = get_user_model().objects.create(username='etudiant1', first_name='etudiant1', email='etudiant@gem-univ-grenoble.fr', password='etudiant1', rgpd_accept="2020-06-25")
        self.user2 = get_user_model().objects.create(username='ensiinfo1', first_name='michel', email='support@ensimag-info.fr', password='matriochka', rgpd_accept="2020-06-25")
        self.affiliation2 = Affiliation.objects.create(name="Grenoble INP", type="Ecole")
        self.user2.affiliations.add(self.affiliation2)
        self.user2.save()
        self.affiliation = Affiliation.objects.create(name='cnrs', type='Recherche' )
        self.view = UserViewSet.as_view(actions={'patch': 'partial_update'})
        self.rgpd_accept_date = datetime.date(2020,6,24)
        self.lig_entity = Entity.objects.create(name = 'LIG', description = 'Laboratoire Informatique de Grenoble', contact='contact-lig@univ-grenoble-alpes.fr')
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.superuser.rgpd_accept = timezone.now().date()
        self.superuser.save()

    def test_update_self_affiliations(self):
        """
        Test de la modification d'une affiliation
        """
        data = { 'affiliations' : [self.affiliation.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_user_affiliation(self):
        """
        Test de la protection de l'affiliation d'un autre utilisateur
        """
        data = { 'affiliations' : [self.affiliation2.pk] }
        request = self.apiFactory.patch(reverse('user-detail', args=(self.user.id, 'pk')),data)
        force_authenticate(request, user=self.user2)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_rgpd_acceptance_input(self):
        """
        Test du format de la date envoyée
        """
        data = { 'rgpd_accept' : 'True' }
        request = self.apiFactory.patch(reverse('user-detail', args=(2, 'pk')),data)
        force_authenticate(request, user=self.superuser)
        response = self.view(request, pk=self.user.id)
        response.render()
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)



class AffiliationsTests(APITestCase):

    def api_factory(self):
        return APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        self.apiFactory = self.api_factory()
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.superuser.rgpd_accept = timezone.now().date()
        self.superuser.save()
        self.affiliation = Affiliation.objects.create(name='Grenoble INP', type='Ecole')
        self.user =  get_user_model().objects.create(username="max", first_name="max", email='max@univ-grenoble.fr', password='1ngF@b', rgpd_accept="2020-06-25")

    def test_affiliation_add(self):
        """
        Test de l'ajout d'une affiliation par un admin
        """
        data = { 'name': 'CNRS', 'type': 'Recherche' }
        view = AffiliationViewSet.as_view(actions={'post': 'create'})
        request = self.apiFactory.post(reverse('affiliation-list'), data)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_affiliation_update(self):
        """
        Test de la modification d'une affiliation par un admin
        """
        data = { 'name' : 'UGA' }
        view = AffiliationViewSet.as_view(actions={'patch': 'partial_update'})
        request = self.apiFactory.patch(reverse('affiliation-detail', args=(1, 'pk')), data)
        force_authenticate(request, user=self.superuser)
        response = view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_affiliation(self):
        "Test de la protection modification d'affiliation par un utilisateur sans droit"
        data = { 'name' : 'Grenoble INP' }
        view = AffiliationViewSet.as_view(actions={'patch': 'partial_update'})
        request = self.apiFactory.patch(reverse('affiliation-detail', args=(1, 'pk')),data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.user.pk)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_add_affiliation(self):
        "Test de la protection ajout d'affiliation par un utilisateur sans droit"
        data = { 'name' : 'Inria Grenoble', 'type':'Recherche' }
        view = AffiliationViewSet.as_view(actions={'post': 'create'})
        request = self.apiFactory.post(reverse('affiliation-list'),data)
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GenericMaterialsTests(APITestCase):

    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.manager2 = get_user_model().objects.create(username="malik", first_name="manager2",email="malik-fabmstic@univ-grenoble-alpes.fr")
        self.manager1.rgpd_accept = timezone.now().date()
        self.manager1.save()
        self.manager2.rgpd_accept = timezone.now().date()
        self.manager2.save()

        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1', rgpd_accept="2020-06-25")
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
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_modify_material(self):
        """
        Test de la modification d'un équipement par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = {'name':'Série SC-1608'}
        response = self.client.patch(reverse('genericmaterials-detail', kwargs={'entity_pk':1, 'pk' : 1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_add_material(self):
        """
        Test de l'ajout d'un équipement par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'FabMSTIC', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire','quantity':'5', 'entity': 1}
        response = self.client.post(reverse('genericmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_not_add_material(self):
        """
        Test de la protection d'ajout d'un équipement
        """
        self.client.force_authenticate(user=self.user)
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'FabMSTIC', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire','quantity':'5', 'entity': 1}
        response = self.client.post(reverse('genericmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_not_update_material(self):
        """
        Test de la protection de modification d'un équipement
        """
        self.client.force_authenticate(user=self.manager2)
        data = {'name':'Ensimag'}
        response = self.client.patch(reverse('genericmaterials-detail', kwargs={'pk': 1, 'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # def test_available_generic_material
        # test pour retourner la disponibilité d'un matériel sur des dates données

class SpecificMaterialsTests(APITestCase):

    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.manager2 = get_user_model().objects.create(username="malik", first_name="manager2",email="malik-fabmstic@univ-grenoble-alpes.fr")
        self.manager1.rgpd_accept = timezone.now().date()
        self.manager1.save()
        self.manager2.rgpd_accept = timezone.now().date()
        self.manager2.save()

        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1', rgpd_accept="2020-06-25")
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
        material_specific = {"name": "filmeuse plastique A4","ref_int":"A4-Fellowes","ref_man":"410-A4RET","localisation":"Etagere 2 - box 4","description":"Filmeuse format A4/A5 ","entity":self.entity.id}
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':1}), material_specific)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_not_add_material(self):
        """
        Test de la protection d'ajout de matériel spécifique
        Rejet si doublon du nom existant par entité
        self.client.force_authenticate(user=self.manager2)
        """
        data = {'name':'iSAFT SpW', 'ref_int':'iSAFT-PCIE-FabMSTIC', 'ref_man':'TELETEL', 'localisation':'armoire box électronique, 3eme etage - deuxieme tiroir ', 'description':'Cartes d’interface PCIe iSAFT à 4 ou 8 ports SpaceWire', 'entity': 1}
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        # test champs unique nom matériel et entité
        self.client.force_authenticate(user=self.manager1)
        data = serializers.serialize('json', [ self.materials_specific, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('specificmaterials-list', kwargs={'entity_pk':1 }), material)
        response.render()
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']),1)

    def test_not_update_material(self):
        """
        Test de la protection de modification de matériel spécifique
        """
        self.client.force_authenticate(user=self.manager2)
        data = {'name':'Tablette ASUS'}
        response = self.client.patch(reverse('specificmaterials-detail', kwargs={'pk': 1, 'entity_pk':1}), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_add_instance_material(self):
        """
        Test de l'ajout d'une instance équipement spécifique par un manager
        """
        self.client.force_authenticate(user=self.manager1)
        materials_specific_instance = {"model":self.materials_specific.pk, "name":"carte ARM/FPGA Soc 2", "serial_num":"002234", "description":'instance2 carte FPGA Phelma'}
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk }), materials_specific_instance)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_not_add_instance_material(self):
        """
        Test de la protection d'ajout d'une instance de matériel spécifique par un utilisateur non manager
        Rejet si nom de l'Instance appartenant à l'entité non unique
        """
        self.client.force_authenticate(user=self.manager2)
        data = serializers.serialize('json', [ self.materials_specific_instance, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk }), material)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        # test champs unique nom instance et materiel spécifique
        self.client.force_authenticate(user=self.manager1)
        data = serializers.serialize('json', [ self.materials_specific_instance, ])
        struct = json.loads(data)
        material = struct[0]['fields']
        response = self.client.post(reverse('instances-list', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk }), material)
        response.render()
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']),1)

    def test_not_update_instance_material(self):
        """
        Test de la protection d'ajout d'une instance de matériel spécifique par un utilisateur non manager
        """
        self.client.force_authenticate(user=self.manager2)
        data = {'name': 'Xtion PRO LIVE'}
        response = self.client.patch(reverse('instances-detail', kwargs={'entity_pk':1, 'specificmaterial_pk': self.materials_specific.pk, 'pk': self.materials_specific_instance.pk }), data)
        response.render()
        # OK
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

class LoanMaterialsTests(APITestCase):

    def setUp(self):
        #ajout de managers
        self.manager1 = get_user_model().objects.create(username="manager1", first_name="manager1",email="manager1@grenoble-inp.fr")
        self.manager1.rgpd_accept = timezone.now().date()
        self.manager1.save()
        self.manager2 = get_user_model().objects.create(username="manager2", first_name="manager2",email="manager2@grenoble-inp.fr")
        self.manager2.rgpd_accept = timezone.now().date()
        self.manager2.save()
        self.user =  get_user_model().objects.create(username="ingenieur1", first_name="ingenieur1", email='ingenieur1@univ-grenoble.fr', password='ingénieur1')
        self.user.rgpd_accept = timezone.now().date()
        self.user.save()
        self.entity = Entity.objects.create(name="ENSAG", description="Ecole Architecture Enseignement Sup",contact="contact@grenoble.archi.fr")
        self.entity.managers.add(self.manager1)
        self.entity.save()
        self.materials_specific = SpecificMaterial.objects.create(name="Zybo ARM/FPGA SoC",ref_int="410-279-RET-PHELMA1",ref_man="410-279-RET",localisation="Etagere 2 - box 4",description="Plateforme programmable FPGA",entity=self.entity)
        self.materials_specific_instance = SpecificMaterialInstance.objects.create(model=self.materials_specific, name="carte ARM/FPGA Soc 1", serial_num="002234", description='instance carte FPGA Phelma' )
        self.materials_generic = GenericMaterial.objects.create(name="Module RF433,",ref_int="MHZRF433",ref_man="SparkFunMZ433",localisation="FabMSTIC",description="Module radio 433MHZ",quantity="20",entity=self.entity)
        self.materials_specific2 = SpecificMaterial.objects.create(name="Epson projector EBS31 RM1250,",ref_int="EBS31-RM1250_ensag",ref_man="EBS31-RM1250",localisation="perForm - salle matériels video - 1er etage",description="Besoin d'un adaptateur screenbeam pour fonctionner",entity=self.entity)
        self.materials_specific_instance2 = SpecificMaterialInstance.objects.create(model=self.materials_specific2, name="Epson projector EBS31 RM1250", serial_num="002234", description='instance Epson projector EBS31 RM1250 Ensag' )
        self.materials_generic_2 =  GenericMaterial.objects.create(name="Détecteur DHT22,",ref_int="dht22_aip",ref_man="dht22_stutt",localisation="FabMSTIC",description="Capteur qualité air",quantity="0",entity=self.entity)

        self.loan = Loan.objects.create(status=3, checkout_date = datetime.date(2020,6,8), user=self.user,entity=self.entity, due_date=datetime.date(2020,6,24), return_date=datetime.date(2020,6,24), comments='demande de prêt cours arts visuel')
        self.loan.specific_materials.add(self.materials_specific_instance)
        self.loan.save()

        self.loan2 = Loan.objects.create(status=2, checkout_date = datetime.date(2020,6,8), user=self.user,entity=self.entity, due_date=datetime.date(2020,6,24), return_date=datetime.date(2020,6,24), comments='demande de prêt cartes STM32 cours info/iot master ensimag')
        self.loan2.save()

        self.entity2 = Entity.objects.create(name="UGA", description="Univ Grenoble Alpes",contact="contact@univ-grenoble.alpes.fr")
        self.entity2.managers.add(self.user)
        self.entity2.save()
        self.loan_manager = Loan.objects.create(status=2, checkout_date = datetime.date(2020,10,8), user=self.manager1,entity=self.entity, due_date=datetime.date(2020,10,24), return_date=datetime.date(2020,10,24), comments='demande de prêt tablettes info')
        self.loan_manager.specific_materials.add(self.materials_specific_instance2)
        self.loan_manager.save()
        self.loan_manager2 = Loan.objects.create(status=2, checkout_date = datetime.date(2020,10,8), user=self.manager2,entity=self.entity, due_date=datetime.date(2020,10,24), return_date=datetime.date(2020,10,24), comments='demande de prêt matériel générique')
        self.loan_manager2.generic_materials.add(self.materials_generic)
        self.loan_manager2.save()
        self.loan_manager_2 = Loan.objects.create(status=3, checkout_date=datetime.date(2020,10,11), user=self.manager1, entity=self.entity, due_date=datetime.date(2021,2,1), return_date=datetime.date(2020,12,10), comments='changement de projecteur')
        self.loan_manager_2.specific_materials.add(self.materials_specific_instance2)
        self.loan_manager_2.save()
        self.loan_user = Loan.objects.create(status=2, checkout_date = datetime.date(2020,6,25), user=self.user,entity=self.entity, due_date=datetime.date(2020,7,24), return_date=datetime.date(2020,8,24), comments='demande de prêt tablettes info', parent=self.loan)
        self.loan_user.specific_materials.add(self.materials_specific_instance)
        self.loan_user.save()
        self.loan_user_accepted = Loan.objects.create(status=3, checkout_date = datetime.date(2020,8,25), user=self.user,entity=self.entity, due_date=datetime.date(2020,9,24), return_date=datetime.date(2020,9,24), comments='demande de prêt tablettes info', parent=self.loan_user)
        self.loan_user_accepted.specific_materials.add(self.materials_specific_instance)
        self.loan_user_accepted.save()
        self.client = APIClient()

    def test_return_date(self):
        """
        date de retour et date de rendu doivent être après la date de sortie
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,10,8), "user" : self.user.pk , "entity" : 1, "due_date" : datetime.date(2020,6,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEqual(response.status_code, 400)
        data = {"status" : 2, "checkout_date" : datetime.date(2020,10,8), "user" : self.user.pk , "entity" : 1, "due_date" : datetime.date(2020,10,18), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEqual(response.status_code, 400)

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
                self.assertEqual(value['fields']['entity'], self.entity.pk)

    def test_create_loan_status(self):
        """
        un utilisateur peut uniquement créer des prêts avec le status requested
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,25), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,25), "return_date" : datetime.date(2020,7,25), "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEqual(response.data['status'], 2)

    def test_create_loan_zeroquantity(self):
        """
        un utilisateur peut faire une demande de prêt d'un matériel générique sans quantité prise en compte
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,25), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,25), "return_date" : datetime.date(2020,7,25), "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [], 'generic_materials': [{"material": self.materials_generic.pk, "quantity": 2 }, { "material": self.materials_generic_2.pk, "quantity": 1 }] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()

        loan_id = response.data['id']
        self.assertEqual(response.data['status'], 2)

        data["status"] = 3
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': loan_id}), data)
        response.render()

        loan = Loan.objects.get(id=loan_id)
        genmats = loan.generic_materials.all()
        self.assertEqual(genmats[1].quantity, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_loan_status(self):
        """
        un utilisateur peut uniquement modifier des prêts avec le status pending
        """
        data = { "status" : 2, "id": self.loan_user.pk, "checkout_date" : datetime.date(2020,6,26), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,24), "comments" : 'modification pret 1', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}),data)
        response.render()
        self.assertEqual(response.data['status'], 2)

    def test_empty_loan(self):
        """
        un prêt doit contenir au moins un matériel
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,9,24), "return_date" : datetime.date(2020,9,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan2.pk }), data)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_indem_adduser_loan(self):
        """
        un utilisateur ne peut modifier un prêt pour un autre utilisateur
        """
        data = {"status" : 2, "id": self.loan.pk, "checkout_date" : datetime.date(2020,6,8), "user" : self.manager1.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,6,24), "return_date" : datetime.date(2020,6,24), "comments" : 'modification pret 1', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}),data)
        response.render()
        self.assertEqual(response.data['user'], self.user.pk)

    def test_update_loan_accepted(self):
        """
        un prêt accepté ne peut être modifié par un utilisateur sans droits
        """
        data = {"status" : 2, "id": self.loan.pk , "checkout_date" : datetime.date(2020,6,9), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,6,24), "return_date" : datetime.date(2020,6,25), "comments" : 'modification prêt accepté', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_child_loan_update(self):
        """
        un prêt enfant peut être modifié si il a le statut pending
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,7,8), "user" : self.manager1.pk , "entity" : 1, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,7,24), "comments" : 'modification prêt enfant', 'specific_materials': [self.materials_specific_instance2.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user.pk }), data, format='json')
        response.render()
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['status'], 2)


    def test_indem_update_accepted_loan(self):
        """
        un prêt ne peut être modifié si il a le status accepté
        """
        data = {"status" : 3, "checkout_date" : datetime.date(2020,9,24), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,10,14), "return_date" : datetime.date(2020,10,14), "comments" : 'modification pret 1', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan_user_accepted.pk}),data)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_manage_loan(self):
        """
        le manager d'une entité peut créer un prêt rattaché à cette entité pour une autre personne
        """
        data = {"status" : 2, "id": self.loan.pk ,"checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande de prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data, format='json')
        response.render()
        self.assertEqual(response.data['user'], self.user.pk)

    def test_own_user_loans(self):
        """
        un utilisateur ne peut voir uniquement les prêts qui lui sont rattachés
        """

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('loan-list'), format='json')
        response.render()
        self.assertEqual(len(response.data), 4)

    def test_own_manager_loans(self):
        """
        le manager d'une entité peut crée/modifier/supprimer les prêts ratachés à son entité
        """

        data = {"status" : 2, "id": self.loan.pk, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,6,24), "comments" : 'demande prêt cours arts visuel', 'specific_materials': [self.materials_specific_instance.pk, self.materials_specific_instance2.pk], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.patch(reverse('loan-detail', kwargs={'pk': self.loan.pk }), data, format='json')
        response.render()
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = {"status" : 2, "checkout_date" : datetime.date(2020,9,24), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,10,15), "return_date" : datetime.date(2020,10,16), "comments" : 'prêt n°2 ', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_child_loan(self):
        """
        Seul un manager peut créer un prêt successeur
        Vérification de la même entité pour la copie du prêt
        """
        data = {"status" : 3, "checkout_date": datetime.date(2020,8,25), "user" : self.user.pk, "entity": self.entity.pk, "due_date": datetime.date(2020,9,24), "return_date" : datetime.date(2020,9,24), "comments" : 'demande de prêt tablettes info'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-make-child', kwargs= {'pk': self.loan_user_accepted.pk}), data)
        response.render()
        self.assertEqual(response.data['parent']['id'], self.loan_user_accepted.pk),

    def test_protected_loan_return_date(self):
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,26), "comments" : 'modification date retour', 'specific_materials': [], 'generic_materials': [{"material":self.materials_generic.pk, "quantity":1}]}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail',  kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEqual(response.data['return_date'], "2020-08-24")

    def test_protected_loan_parent(self):
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,26), "comments" : 'modification date retour', 'specific_materials': [], 'generic_materials': [{"material":self.materials_generic.pk, "quantity":1}],  'parent': self.loan_manager.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('loan-detail',  kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEqual(response.data['parent'], self.loan.pk)

    def test_protected_loan_user(self):
        """
        un utilisateur ne peut modifier les champs, parent, return_date et
        user (transfert vers un autre utilisateur)
        """
        # test protection utilisateur
        data = {"status" : 2, "checkout_date" : datetime.date(2020,6,8), "user" : self.manager2.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,7,24), "return_date" : datetime.date(2020,8,24), "comments" : 'prolongation du prêt de tablettes, ajout de retroprojecteur', 'specific_materials': [], 'generic_materials': [{"material": 1, "quantity": 10}] }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('loan-detail', kwargs={'pk': self.loan_user.pk}), data)
        response.render()
        self.assertEqual(response.data['user'], self.user.pk)

    def test_specific_material_instance(self):
        """
        un material spécifique ne peut être emprunté en meme temps
        """
        data = {"status" : 3, "checkout_date" : datetime.date(2020,5,2), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,5,5), "return_date" : None, "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()

        data = {"status" : 2, "checkout_date" : datetime.date(2020,5,3), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,5,6), "return_date" : None, "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"status" : 2, "checkout_date" : datetime.date(2020,5,1), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,5,4), "return_date" : datetime.date(2020,5,5), "comments" : 'demande de prêt projet etudes Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_available_specific_material(self):
        """
        Si un prêt arrive à date échue, le matériel lié est de nouveau disponible
        """
        data = {"status" : 2, "checkout_date" : datetime.date(2020,9,24), "user" : self.user.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,10,4), "return_date" : datetime.date(2020,10,4), "comments" : 'demande de prêt tablettes projet Master 1 Ensimag', 'specific_materials': [self.materials_specific_instance.pk], 'generic_materials': [] }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_delete_loan_requested(self):
        """
        Un utilisateur ne peut supprimer un prêt demandé ou accepté
        """
        self.client.force_authenticate(user=self.manager2)
        response = self.client.get(reverse('loan-detail',kwargs={'pk': self.loan_manager2.pk}))
        response.render()
        response = self.client.delete(reverse('loan-detail',kwargs={'pk': self.loan_manager2.pk}))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.force_authenticate(user=self.user)
        loan = self.client.get(reverse('loan-detail', kwargs={'pk': self.loan_user_accepted.pk}))

        response = self.client.delete(reverse('loan-detail',kwargs={'pk': self.loan_user_accepted.pk}))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_loan_requested(self):
        """
        Un manager peut supprimer un prêt demandé ou accepté
        """
        self.client.force_authenticate(user=self.manager1)
        response = self.client.delete(reverse('loan-detail',kwargs={'pk': self.loan_user.pk}))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #test de la protection suppression prêt refusé

    def test_material_availability(self):
        """
        Test la disponibilité d'un matériel avec une date de retour
        """
        self.client.force_authenticate(user=self.manager1)
        data = {"status" : 3, "checkout_date" : datetime.date(2020,10,8), "user" : self.manager1.pk , "entity" : self.entity.pk, "due_date" : datetime.date(2020,10,9), "return_date" : datetime.date(2020,12,20), "comments" : 'demande de prêt projecteur cours Polytech', 'specific_materials': [self.materials_specific_instance2.pk], 'generic_materials': [] }
        response = self.client.post(reverse('loan-list'), data, format='json')
        response.render()
        self.assertGreater(datetime.date(2020,12,10), datetime.date(2020,11,11))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
