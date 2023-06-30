# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import (
    RGPDAccept)

from .purge_db import *
from .stats_utils.recup_params_tools import params_request_entity

class PurgeViewSet(viewsets.ViewSet):
    """
    paramètre obligatoire : 
        - entity_selected (paramètre qui correspond à l'entité dont l'utilisateur est manager et dont il souhaite consulter les statistiques)
            => valeur de type integer (clé primaire de Entity)
    """
    permission_classes = (RGPDAccept,)

    "###################### Traitement d'une demande de statistique de type Nombre d'Emprunt ######################"
    @action(methods=['get'], detail=False)
    def dl_archive(self, request):
        try:
            entity_sel = params_request_entity(request)
            return Response(anonymous_loans(entity_sel),status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['get'], detail=False)
    def purge_db(self,request):
        msg = purge_all()
        return Response(msg,status=status.HTTP_200_OK)