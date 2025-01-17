"""
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
import json
from io import StringIO
import csv

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.core.management import call_command
from django.db.models.signals import post_save
from django.dispatch import receiver

import rest_framework
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAdminUser
from rest_framework import viewsets, mixins, status, generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError, NotFound
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ParseError

from .models import (
    Entity,
    Affiliation,
    Tag,
    SpecificMaterial,
    SpecificMaterialInstance,
    GenericMaterial,
    Loan,
    LoanGenericItem)
from .serializers import *
from .permissions import (
    EntityPermission,
    RGPDAccept,
    IsManagerCreateOrReadOnly,
    IsManager,
    IsManagerOf,
    IsAdminOrIsSelf,
    IsAdminOrReadOnly,
    LoanPermission)
from .emails import Emails


class EntityFilterBackend(filters.BaseFilterBackend):
    """
    Filter against entity
    """

    def filter_queryset(self, request, queryset, view):
        entityid = request.query_params.get('entity', None)
        if entityid is not None:
            try:
                entityid = int(entityid)
                return queryset.filter(entity__id=entityid).distinct()
            except ValueError:
                pass
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search is None:
            if 'pk' in self.kwargs:
                # Used to get a single user, for create a new loan
                return get_user_model().objects.filter(
                    pk=self.kwargs['pk']).distinct()
            elif self.request.user.is_staff:
                return get_user_model().objects.all()
            else:
                searchQ = Q(
                    pk=self.request.user.id) | Q(
                    loans__entity__in=self.request.user.entities.values_list(
                        'id', flat=True)) | Q(
                    entities__in=self.request.user.entities.values_list(
                        'id', flat=True))

                return get_user_model().objects.filter(searchQ).distinct()
        else:
            if (len(search) < 3):
                return get_user_model().objects.none()
            searchQ = Q(
                pk=self.request.user.id) | Q(
                username__icontains=search) | Q(
                first_name__icontains=search) | Q(
                last_name__icontains=search)
            return get_user_model().objects.filter(searchQ).distinct()

    def get_serializer_class(self):
        """
        Non admin user cannot see private user attribute for privacy reason
        """
        if self.action == "list" and not self.request.user.is_staff:
            return UserPublicSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsManager]
        elif self.action in ['update', 'partial_update', 'set_password']:
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
                if not user.check_password(
                        serializer.data.get('old_password')):
                    return Response({'old_password': ['Wrong password.']},
                                    status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'status': 'password set'},
                                status=status.HTTP_200_OK)

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
            username = (lastname[:7] + firstname[0]).lower()
            count = 2
            while (get_user_model().objects.filter(
                    username=username).exists()):
                username = (lastname[:7] + firstname[0]).lower() + str(count)
                count = count + 1
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


class RGPDAcceptView(APIView):
    """
    Endpoint to accept rgpd conditions
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.user.rgpd_accept is None and 'accept' in request.data:
            if request.data['accept']:
                request.user.rgpd_accept = timezone.now().date()
                request.user.save()
        return Response({"rgpd_accept": request.user.rgpd_accept})

    def get(self, request, format=None):
        return Response({"rgpd_accept": request.user.rgpd_accept})


class PersonalDataView(APIView):
    """
    Endpoint to get personal related data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        instance = UserDataSerializer(
            request.user, context={'request': request})
        return Response({"user": instance.data})


class EntityViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the entities
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = (RGPDAccept, EntityPermission,)
    search_fields = ['name']
    ordering_fields = ['name']

    def get_queryset(self):

        # If user is not pro and not specific search (for old loan), hide
        # entity
        ids_q = self.request.query_params.get('ids', None)
        if (ids_q is None and not self.request.user.is_pro):
            return Entity.objects.all().filter(is_pro=False)
        else:
            return Entity.objects.all()


class AffiliationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows affiliations to be viewed or edited.
    """
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    permission_classes = (RGPDAccept, IsAdminOrReadOnly,)
    search_fields = ['name']
    ordering_fields = ['name', 'type']

    @action(methods=['get'], detail=False)
    def types(self, request):
        """
        Return the affiliation types
        """
        return Response(
            dict(
                (x,
                 y) for x,
                y in Affiliation.TYPE_AFFILIATION),
            status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the material tags
    """
    queryset = Tag.objects.all()
    permission_classes = (RGPDAccept, IsManagerCreateOrReadOnly,)
    serializer_class = TagSerializer
    search_fields = ['name']
    ordering_fields = ['name']

    @action(methods=['delete'], detail=False)
    def delete_unused(self, request):
        """
        Special end point for deleteing unused tag
        return list of ids of deleted tags
        """
        if request.user.is_staff:
            unusedtags = Tag.objects.filter(
                genericmaterials=None, specificmaterials=None)
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
        if not self.request.user.is_staff and self.request.user not in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        return self.queryset.filter(entity=entity)

    def create(self, request, *args, **kwargs):
        """
        Check if the current user is an admin or if he is a manager of the entity
        Overide the entity props of the material to the one in the url
        """
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and self.request.user not in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        request.data.update({'entity': self.kwargs['entity_pk']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Avoid the entity prop to be updated (transfert of material beetween entities)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data.update({'entity': instance.entity.id})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
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
    permission_classes = (RGPDAccept, IsManagerOf,)
    serializer_class = GenericMaterialSerializer
    search_fields = ['name', 'ref_man', 'ref_int']
    ordering_fields = ['name']

    @action(methods=['post'], detail=False,
            parser_classes=[MultiPartParser, FormParser, FileUploadParser])
    def bulk_add(self, request, *arg, **kwargs):
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and self.request.user not in entity.managers.all():
            raise PermissionDenied("Vous n'êtes pas manager de cette entité")
        data = None
        text = None
        if ('file' in request.data):
            try:
                text = request.data['file'].read().decode('utf-8')
            except UnicodeDecodeError:
                raise ParseError("Le fichier doit être encoder en utf-8")
        elif ('text' in request.data):
            text = request.data['text']
        if (text):
            try:
                f = StringIO(text)
                data = list(csv.reader(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL))
            except BaseException:
                raise ParseError("Fichier csv au mauvais format")
            rows = data
            if (rows and rows[0] and rows[0][0] == "name"):
                rows.pop(0)
            tags_dict = {}
            mats = []
            matnames = []
            mats_tags = []
            try:
                for row in rows:
                    if len(row) != 7:
                        print("wrong format" + str(len(row)))
                        raise ParseError("Wrong CSV format")
                    row = list(v if v else None for v in row)
                    row[1] = 0 if row[1] is None else row[1]
                    mat = GenericMaterial(name=row[0],
                                          quantity=row[1],
                                          ref_int=row[2],
                                          ref_man=row[3],
                                          description=row[4],
                                          localisation=row[5],
                                          entity=entity
                                          )
                    matnames.append(mat.name)
                    mats.append(mat)
                    if (row[6]):
                        tagstrs = list(t.strip() for t in row[6].split(","))
                        tags = []
                        for tagstr in tagstrs:
                            if tagstr in tags_dict:
                                tags.append(tags_dict[tagstr])
                            else:
                                tag, created = Tag.objects.get_or_create(
                                    name=tagstr)
                                tags_dict[tagstr] = tag
                                tags.append(tag)
                        mats_tags.append(tags)
                    else:
                        mats_tags.append([])
            except BaseException:
                raise ParseError(
                    "Une erreur c'est produite lors de l'ajout massif (ex nom déjà existant)")
            names_conflict = GenericMaterial.objects.filter(
                entity=entity, name__in=matnames).values_list(
                'name', flat=True).all()
            if (names_conflict):
                raise ParseError(
                    "Ajout impossible: l'entité contient déjà les matériels " + str(list(names_conflict)))

            try:
                matsdb = GenericMaterial.objects.bulk_create(mats)
                matids = []
                matsret = []
                if (matsdb[0].id is None):
                    for mat in matsdb:
                        matsret.append(GenericMaterial.objects.get(
                            name=mat.name, entity=entity))
                else:
                    matsret = matsdb
                throughs = []
                Modelthrough = GenericMaterial.tags.through
                for i, mat in enumerate(matsret):
                    for tag in mats_tags[i]:
                        throughs.append(Modelthrough(
                            tag_id=tag.id, genericmaterial_id=mat.id))
                Modelthrough.objects.bulk_create(throughs)
                serializer = GenericMaterialSerializer(matsret, many=True)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except BaseException:
                raise ParseError(
                    "Une erreur c'est produite lors de l'ajout massif (ex nom déjà existant)")
        else:
            raise ParseError("Aucune donnée reçue")


class EntitySpecificMaterialViewSet(
        EntityMaterialMixin, viewsets.ModelViewSet):
    """
    Endpoints for specific material
    Use nested router params
    """
    queryset = SpecificMaterial.objects.all()
    permission_classes = (RGPDAccept, IsManagerOf,)
    serializer_class = SpecificMaterialSerializer
    search_fields = ['name', 'ref_int', 'ref_man']
    ordering_fields = ['name']


class EntitySpecificMaterialInstanceViewSet(viewsets.ModelViewSet):
    """
    Endpoints for instance of specific material
    Use nested router params
    """
    queryset = SpecificMaterialInstance.objects.all()
    permission_classes = (RGPDAccept, IsManagerOf,)
    serializer_class = SpecificMaterialInstanceSerializer
    search_fields = ['name', 'serial_num']
    ordering_fields = ['name']

    def get_queryset(self):
        """
        Filter the queryset using entity_pk and specificmaterial_pk of the nested router
        Check if the current user is an admin or if he is a manager of the entity owning the material
        Check if the instance belongs to the specific material id in the nested router params
        """
        entity = get_object_or_404(Entity.objects, pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and self.request.user not in entity.managers.all():
            raise PermissionDenied("You are not a manager of this entity")
        if not entity.specificmaterials.filter(
                id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied(
                "This material does not belong to your entity")
        return self.queryset.filter(
            model__entity=entity, model=self.kwargs['specificmaterial_pk'])

    def create(self, request, *args, **kwargs):
        """
        Check if the current user is an admin or if he is a manager of the entity owning the material
        Check if the instance belongs to the specific material id in the nested router params
        """
        entity = Entity.objects.get(pk=self.kwargs['entity_pk'])
        if not self.request.user.is_staff and self.request.user not in entity.managers.all():
            raise PermissionDenied("Your are not a manager of this entity")
        if not entity.specificmaterials.filter(
                id=self.kwargs['specificmaterial_pk']).exists():
            raise PermissionDenied(
                "This material does not belong to your entity")
        request.data.update({'model': int(self.kwargs['specificmaterial_pk'])})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Avoid the model prop to be updated (transfert of instance beetween material)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data.update({'model': instance.model.id})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LimitOffsetPaginationMulti(LimitOffsetPagination):

    def paginate_queryset(self, querysets, request, view=None):
        self.offset = self.get_offset(request)
        self.limit = self.get_limit(request)
        self.count = 0
        ret = []
        for queryset in querysets:
            self.count = self.count + self.get_count(queryset)
        if self.limit is None:
            for queryset in querysets:
                ret.append([])
            return tuple(ret)

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        if self.count == 0 or self.offset > self.count:
            ret = []
            for queryset in querysets:
                ret.append([])
            return tuple(ret)
        locoffset = self.offset
        loclimit = self.limit
        for queryset in querysets:
            if locoffset >= self.get_count(queryset):
                ret.append([])
                locoffset = locoffset - self.get_count(queryset)
            elif loclimit > 0:
                l = []
                if (locoffset + loclimit >= self.get_count(queryset)):
                    l = list(queryset[locoffset:])
                else:
                    l = list(queryset[locoffset:locoffset + loclimit])
                locoffset = 0
                loclimit = loclimit - len(l)
                ret.append(l)
            else:
                ret.append([])

        return tuple(ret)


class RetrieveGenericMaterialsView(generics.RetrieveAPIView):
    queryset = GenericMaterial.objects.filter(active=True)
    permission_classes = (RGPDAccept, IsAuthenticated,)
    serializer_class = GenericMaterialPublicSerializer


class RetrieveSpecificMaterialsView(generics.RetrieveAPIView):
    queryset = SpecificMaterial.objects.filter(active=True)
    permission_classes = (RGPDAccept, IsAuthenticated,)
    serializer_class = SpecificMaterialPublicSerializer


class MaterialsView(APIView):
    permission_classes = (RGPDAccept, IsAuthenticated,)

    def get(self, request, format=None, entity_pk=None):

        entitiesid = []
        if (entity_pk is not None):
            entitiesid = [entity_pk]
            entity = get_object_or_404(Entity, pk=entity_pk)
            if not request.user.is_staff and request.user not in entity.managers.all():
                raise PermissionDenied()
        else:
            entities = request.query_params.getlist('entities[]', None)
            if (entities is not None):
                ents = entities
                try:
                    for i, v in enumerate(ents):
                        ents[i] = int(v)
                    entitiesid = ents
                except BaseException:
                    pass
        # Specific search
        # hidden and is_pro not checked to always be able to show an old loan
        # TODO if user not manager only show materiel in own loans
        loanid = request.query_params.get('loan', None)
        loan = None
        if (loanid is not None):
            try:
                loanid = int(loanid)
                loan = get_object_or_404(Loan, pk=loanid)
            except BaseException:
                raise ParseError(loanid + ' not a number')

        gms = request.query_params.get('gmids', None)
        gmids = []
        if (gms is not None):
            gmst = gms.split(',')
            try:
                for i, v in enumerate(gmst):
                    gmst[i] = int(v)
                gmids = gmst
            except BaseException:
                pass
        sms = request.query_params.get('smids', None)
        smids = []
        if (sms is not None):
            smst = sms.split(',')
            try:
                for i, v in enumerate(smst):
                    smst[i] = int(v)
                smids = smst
            except BaseException:
                pass

        genmats = GenericMaterial.objects.all()
        spemats = SpecificMaterial.objects.all()

        if loan:
            genmats = genmats.filter(pk__in=loan.generic_materials.all())
            spemats = spemats.filter(instances__loans__in=[loan]).distinct()
        elif gmids or smids:
            genmats = genmats.filter(pk__in=gmids)
            spemats = spemats.filter(pk__in=smids)

        if (not (loan or gmids or smids)):
            # Search Mode
            search = request.query_params.get('search', None)

            hidden = request.query_params.get('hidden', False)

            if hidden and hidden != "true":
                hidden = False

            mattype = request.query_params.get('type', None)
            if (mattype is not None and mattype != 's' and mattype != 'g'):
                mattype = None

            tags = request.query_params.getlist('tags[]', None)
            if (tags is not None):
                tagsid = tags
                try:
                    for i, v in enumerate(tagsid):
                        tagsid[i] = int(v)
                except BaseException:
                    pass

            if mattype:
                if mattype == 'g':
                    spemats = spemats.none()
                elif mattype == 's':
                    genmats = genmats.none()

            if (not request.user.is_pro):
                genmats = genmats.filter(entity__is_pro=False)
                spemats = spemats.filter(entity__is_pro=False)

            if not hidden:
                genmats = genmats.filter(active=True)
                spemats = spemats.filter(active=True)

            if search:
                searchQ = Q(name__icontains=search) | Q(
                    ref_int__icontains=search) | Q(ref_man__icontains=search)
                genmats = genmats.filter(searchQ)
                spemats = spemats.filter(searchQ)
            if entitiesid:
                genmats = genmats.filter(entity__in=entitiesid)
                spemats = spemats.filter(entity__in=entitiesid)

            if tagsid:
                for tid in tagsid:
                    genmats = genmats.filter(tags__in=[tid])
                    spemats = spemats.filter(tags__in=[tid])
            
            genmats = genmats.distinct()
            spemats = spemats.distinct()

        genmats = genmats.order_by("-id")
        paginator = LimitOffsetPaginationMulti()
        genmats, spemats = paginator.paginate_queryset(
            [genmats, spemats], request)

        if (entity_pk is not None):
            genmatsser = GenericMaterialSerializer(genmats, many=True)
            spematsser = SpecificMaterialSerializer(spemats, many=True)
        else:
            genmatsser = GenericMaterialPublicSerializer(genmats, many=True)
            spematsser = SpecificMaterialPublicSerializer(spemats, many=True)

        return paginator.get_paginated_response(
            {"generic_materials": genmatsser.data, "specific_materials": spematsser.data})


class MaterialFilterBackend(filters.BaseFilterBackend):
    """
    Filter against materials
    """

    def filter_queryset(self, request, queryset, view):
        # Filter generic material
        gmid = request.query_params.get('gm', None)
        if gmid is not None:
            try:
                gmid = int(gmid)
                return queryset.filter(generic_materials__id=gmid).distinct()
            except ValueError:
                pass
        # filter specific material instance
        smiid = request.query_params.get('smi', None)
        if smiid is not None:
            try:
                smiid = int(smiid)
                return queryset.filter(specific_materials__id=smiid).distinct()
            except ValueError:
                pass
        # filter specific material
        smid = request.query_params.get('sm', None)
        if smid is not None:
            try:
                smid = int(smid)
                return queryset.filter(
                    specific_materials__model__id=smid).distinct()
            except ValueError:
                pass
        return queryset


class DateFilterBackend(filters.BaseFilterBackend):
    """
    Filter against date
    """

    def filter_queryset(self, request, queryset, view):
        params = {}
        dd = request.query_params.get('dd', None)
        dds = request.query_params.get('dds', 'l')
        if dds == 'l':
            dds = '__lte'
        elif dds == 'g':
            dds = '__gte'
        else:
            dds = ''
        if dd is not None:
            params['due_date' + dds] = dd

        cd = request.query_params.get('cd', None)
        cds = request.query_params.get('cds', 'g')
        if cds == 'l':
            cds = '__lte'
        elif cds == 'g':
            cds = '__gte'
        else:
            cds = ''
        if cd is not None:
            params['checkout_date' + cds] = cd

        rd = request.query_params.get('rd', None)
        rds = request.query_params.get('rds', 'l')
        if rds == 'l':
            rds = '__lte'
        elif rds == 'g':
            rds = '__gte'
        elif rds == 'null':
            rds = '__isnull'
            rd = True
        else:
            rds = ''
        if rd is not None:
            params['return_date' + rds] = rd
        if params:
            queryset = queryset.filter(**params).distinct()

        return queryset


class StatusFilterBackend(filters.BaseFilterBackend):
    """
    Filter against status
    """

    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status', None)
        if status is not None and status != "":
            try:
                status = int(status)
                return queryset.filter(status=status).distinct()
            except ValueError:
                pass
        return queryset


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Filter against user
    """

    def filter_queryset(self, request, queryset, view):
        userid = request.query_params.get('user', None)
        if userid is not None:
            try:
                userid = int(userid)
                return queryset.filter(user=userid).distinct()
            except ValueError:
                pass
        return queryset


class TagFilterBackend(filters.BaseFilterBackend):
    """
    Filter against material tag
    """

    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get('tags', None)
        tagsid = []
        if (tags is not None):
            tagst = tags.split(',')
            try:
                for i, v in enumerate(tagst):
                    tagst[i] = int(v)
                tagsid = tagst
                searchQ = Q(specific_materials__tags__in=tagsid) | Q(
                    generic_materials__tags__in=tagsid)
                return queryset.filter(searchQ).distinct()
            except BaseException:
                pass
        return queryset


class LoanViewSet(viewsets.ModelViewSet):
    """
    Endpoints for loans
    """
    queryset = Loan.objects.all()
    permission_classes = (RGPDAccept, LoanPermission,)
    serializer_class = LoanSerializer
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter,
                       MaterialFilterBackend,
                       EntityFilterBackend,
                       DateFilterBackend,
                       UserFilterBackend,
                       StatusFilterBackend,
                       TagFilterBackend)
    search_fields = ['user__username', 'affiliation__name', 'entity__name']
    ordering_fields = ['due_date', 'return_date', 'checkout_date']

    def get_queryset(self):
        """
        Specific query to filter loans by admin or managers or by current user
        """
        if (self.request.user.is_staff):
            return self.queryset.all()
        return self.queryset.filter(Q(user=self.request.user) | Q(
            entity__managers__in=[self.request.user])).distinct()

    def create(self, request, *args, **kwargs):
        """
        Special action to validate loan creation
        Protect data of current user, set status in requested and set parent, return_date to None value
        If data is valid, loan is created then a notification to entity manager is sent
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if (not request.user.is_staff and request.user not in serializer.validated_data['entity'].managers.all(
        )):
            if serializer.validated_data['user'] != request.user:
                serializer.validated_data['user'] = request.user
            if serializer.validated_data['status'] != Loan.Status.REQUESTED:
                serializer.validated_data['status'] = Loan.Status.REQUESTED
            if serializer.validated_data['return_date']:
                serializer.validated_data['return_date'] = None
            serializer.validated_data['parent'] = None
        if serializer.is_valid():
            manager = request.user.is_staff or request.user in serializer.validated_data['entity'].managers.all(
            )
            loan = serializer.save()
            headers = self.get_success_headers(serializer.data)
            loan.save()
            if not manager:
                Emails.send_manager(loan)
            elif (loan.status == Loan.Status.ACCEPTED):
                Emails.send_status(loan)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Special action to update loan
        Check if current user has rights to perform update
        Protect data of loan user, protect status requested and set parent, return_date with requested data
        If data is valid and status has changed, and not REQUESTED then manager of entity loan is notified by mail
        with update_status_loan
        If status of loan is CANCELED, object is destroyed
        Loan is updated with validated data
        """
        instance = self.get_object()
        if (not request.user.is_staff and request.user not in instance.entity.managers.all()):
            if (instance.status != Loan.Status.REQUESTED):
                raise PermissionDenied(
                    "Vous ne pouvez pas modifier un prêt qui a été accepté, refusé ou annulé")
            request.data.update({'status': int(request.data["status"])})
            request.data.update({'user': instance.user.id})
            request.data.update({'return_date': instance.return_date})
            request.data.update(
                {'parent': instance.parent.id if instance.parent else None})

        hist = request.query_params.get('hist', False)

        partial = kwargs.pop('partial', False)
        if (hist == 'true' and (
                request.user.is_staff or request.user in instance.entity.managers.all())):
            if (hasattr(instance, "child")):
                raise serializers.ValidationError(
                    "Le prêt a déjà un successeur.")
            if (instance.status !=
                    Loan.Status.ACCEPTED or instance.return_date is not None):
                raise serializers.ValidationError(
                    "Vous pouvez copier uniquement un prêt qui a été accepté et non rendu.")
            nowdate = timezone.now().date()
            if (instance.due_date <
                    nowdate):
                raise serializers.ValidationError(
                    "La date de rendu prévu doit être dans le future.")
            # On vérifie que tout est valid sans appliqué les modifications
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            # on cloture le prêt
            instance.return_date = nowdate
            instance.save()
            # on réouvre un nouveau prêt avec date de sortie aujourd'hui
            del request.data['id']
            request.data.update({'checkout_date': nowdate})
            request.data.update({'parent': instance.id})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        else:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            if serializer.is_valid():
                change_status = False
                if (instance.status != request.data["status"]):
                    change_status = True
                loan = self.perform_update(serializer)
                if (change_status):
                    if request.user.is_staff or request.user in serializer.validated_data['entity'].managers.all(
                    ):
                        Emails.send_status(instance)
                    else:
                        # only possible when a user cancel a loan
                        Emails.send_manager(instance)
            if serializer.errors:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (not request.user.is_staff and request.user not in instance.entity.managers.all()):
            if (instance.status == Loan.Status.REQUESTED):
                instance.status = Loan.Status.CANCELED
                instance.save()
                Emails.send_manager(instance)
            else:
                raise PermissionDenied(
                    "Vous ne pouvez pas annuler un prêt qui a été accepté, refusé ou annulé")
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def status(self, request):
        """
        Return the affiliation types
        """
        return Response(
            dict(
                (x,
                 y) for x,
                y in Loan.Status.choices),
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def ask_extension(self, request, pk=None):
        """
        Ask a date extention for the loan
        """
        loan = get_object_or_404(Loan, pk=pk)
        if (loan.status != Loan.Status.ACCEPTED):
            raise serializers.ValidationError(
                "Vous pouvez demander une prolongation uniquement pour un prêt qui a été accepté.")
        try:
            ext_date = date.fromisoformat(request.data['ext_date'])
            if (ext_date <= loan.due_date):
                return Response(
                    "La nouvelle date doit être postérieure à la date de retour prévue",
                    status=status.HTTP_400_BAD_REQUEST)
            Emails.send_extension(loan, ext_date)
            return Response({"message": "Demande envoyée"})
        except BaseException:
            return Response("Mauvais format de date",
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def make_child(self, request, pk=None):
        """
        Create a child of the loan
        Parent/child are used to keep an history for loan modification
        """
        loan = get_object_or_404(Loan, pk=pk)
        if (hasattr(loan, "child")):
            raise serializers.ValidationError("Le prêt a déjà un successeur.")
        if (loan.status != Loan.Status.ACCEPTED):
            raise serializers.ValidationError(
                "Vous pouvez copier uniquement un prêt qui a été accepté.")

        if loan.return_date is None:
            loan.return_date = timezone.now().date()
        loan.save()

        child = Loan.objects.create(
            user=loan.user,
            entity=loan.entity,
            affiliation=loan.affiliation,
            comments=loan.comments,
            status=Loan.Status.ACCEPTED,
            parent=loan,
            due_date=loan.due_date,
            checkout_date=loan.return_date)
        child.specific_materials.set(loan.specific_materials.all())

        mats = []
        for mat in loan.loangenericitem_set.all():
            mats.append(LoanGenericItem(
                loan=child, material=mat.material, quantity=mat.quantity))
        LoanGenericItem.objects.bulk_create(mats)

        sloan = self.get_serializer(loan)
        schild = self.get_serializer(child)

        return Response({"parent": sloan.data, "child": schild.data})


class LoanStatsView(generics.ListAPIView):
    queryset = Loan.objects.all()
    permission_classes = (RGPDAccept, LoanPermission,)
    serializer_class = LoanNestedSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        MaterialFilterBackend,
        EntityFilterBackend,
        DateFilterBackend,
        UserFilterBackend,
        StatusFilterBackend,
        TagFilterBackend)
    search_fields = ['user__username', 'affiliation__name']
    ordering_fields = ['due_date', 'return_date', 'checkout_date']

    def get_queryset(self):
        """
        Specific query to filter loans by admin or managers or by current user
        """
        if (self.request.user.is_staff):
            return self.queryset.all()
        return self.queryset.filter(Q(user=self.request.user) | Q(
            entity__managers__in=[self.request.user])).distinct()
