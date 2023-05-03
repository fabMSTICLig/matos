# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import *
from .permissions import (
    RGPDAccept)

"import outils pour statistiques"
from .stats_utils.data_tools import *
from .stats_utils.recup_params_tools import *
from .stats_utils.generation_tools import *
from .stats_utils.traitements_tri_tools import *

class StatsViewSet(viewsets.ViewSet):
    """
    2 paramètres obligatoires : 
        - tri (paramètre qui correspond au tri souhaité pour un type de statistique donné)
            => valeur de type integer comprise entre 0 et 3 inclus : 
                0 = Affiliation
                1 = Utilisateur
                2 = Objet (Matériel)
                3 = Tag
        - entity_selected (paramètre qui correspond à l'entité dont l'utilisateur est manager et dont il souhaite consulter les statistiques)
            => valeur de type integer (clé primaire de Entity)

    9 paramètres optionnels : 
        - filters_aff (filtres supplémentaires en cas de tri par affiliation, correspond à la liste des types d'affiliation recherchés)
            => valeur de type chaîne pouvant contenir 0,1,2,3,4,5 ou Naff séparés par des virgules :
                0 = Labo (Laboratoire)
                1 = Ecole
                2 = Plateforme
                3 = Service
                4 = Recherche
                5 = Composante (Composante Universitaire)
                Naff = Non affilié (prêts sans affiliations)
            => valeur par défaut = 0,1,2,3,4,5,Naff

        - filter_freq (filtre supplémentaire en cas de calcul de fréquence d'emprunt)
            => valeur de type integer comprise entre 0 et 2 inclus :
                0 = Sans filtre
                1 = Seulement les fréquences supérieures ou égales à 1
                2 = Seulement les fréquences égales à 0
            => valeur par défaut = 0

        - start_d (paramètre qui correspond à la date de début de recherche, la plus lointaine)
            => format jour/mois/année
            => chaque valeur de type integer
            => chaque valeur séparée par un tiret '-' pour coller avec les dates en JS
            => valeur par défaut = date du jour - 3 ans

        - end_d (paramètre qui correspond à la date de fin de recherche, la plus proche)
            => format jour/mois/année
            => chaque valeur de type integer
            => chaque valeur séparée par une virgule ','
            => valeur par défaut = date du jour

        - offset (paramètre correspondant à l'élément de départ de la page)
            => entier positif (int >= 0)
            => valeur par défaut = 0
        
        - reverse_order (paramètre correspond à l'ordre des éléments pour la pagination)
            => n'importe quel type de base = ordre inversé, plus petit au plus grand
            => none ou inexistant = ordre classique, plus grand au plus petit
            => valeur par défaut = ordre classique (False)

        - limit (paramètre correspondant au nombre d'éléments par page)
            => entier positif (int > 0)
            => valeur par défaut = 10

        - clotured (paramètre correspondant à la date de chaque prêt évaluée selon les dates de début et de fin)
            => entier positif compris entre 0 et 2 inclus :
                0 = Date de sortie des prêts
                1 = Date de retour des prêts
                2 = Date de retour et date de sortie des prêts
            => valeur par défaut = 0

        - download (paramètre indiquant à l'api d'envoyer des données téléchargeables non destinées à l'affichage dans l'interface web)
            => Inexistant ou chaîne vide = pas de téléchargement, envoie d'une page à afficher
            => chaîne dans ["pdf","csv","json","txt"], préparation du téléchargement selon format demandé
    """
    permission_classes = (RGPDAccept,)

    "###################### Traitement d'une demande de statistique de type Nombre d'Emprunt ######################"
    @action(methods=['get'], detail=False)
    def nb_emp(self, request):
        """
        ############# Traitement des paramètres de la requête ##############
        """
        """
        Récupération de tous les paramètres
        tri             => type de tri sélectionné
        entity_sel      => entité sélectionnée
        start_date      => date de début de recherche (début plage)
        end_date        => date de fin de recherche (fin plage)
        clotured        => type d'utilisation de la plage de date
        download
        tri_filters_aff 
        """
        all_params = recup_all_params(request)
        "Récupération du cache_name"
        cache_name = gen_cache_name(all_params,"nb_emp")
        "dans le cas où le tri est par affiliation, il faut supprimer le dernier élément du tri_filters_aff, utilisé pour le cache_name"
        if (all_params["tri"] == 0):
            all_params["tri_filters_aff"].pop()

        """
        ############# Traitement de la demande (requête) ##############
        """
        "Dans le cas où une requête identique est stockée dans le cache on la récupère et on la renvoie directement"
        stat = cache.get(cache_name, None)
        if (stat is None):
            """
            dictionnaire de résultats
                chaque clé correspond à un objet de tri, du tri souhaité
                    et est liée à un tableau :
                        en [0] => contient un tableau avec les informations sur l'objet de tri
                        en [1] => la statistique souhaitée
            """
            stat = []
            base_loan = gen_base_loan(all_params)
            
            if (all_params["tri"] == 0):
                stat = trait_global(all_params,base_loan,"nb_emp")

            elif ([1,2,3].count(all_params["tri"]) > 0):
                stat = trait_global(all_params,base_loan,"nb_emp")

            "Tri des valeurs par ordre décroissant"
            stat = sorted(stat, key=lambda item:item[1],reverse=True)
            "Création d'un cache"
            cache.set(cache_name,stat,900)
        "On envoie une réponse"
        if (all_params["download"] != -1):
            try:
                if (all_params["download"] == 0):
                    "Création du tableau 'params_text'"
                    params_text = gen_params_text(all_params)
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],0,params_text,request.user),status=status.HTTP_200_OK)
                else:
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],0),status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(paginate_by(stat,request.query_params.get('offset'),request.query_params.get('reverse_order'),request.query_params.get('limit')),status=status.HTTP_200_OK)
    

    "###################### Traitement d'une demande de statistique de type Durée Moyenne d'Emprunt ######################"
    @action(methods=['get'], detail=False)
    def d_moy_emp(self, request):
        """
        ############# Traitement des paramètres de la requête ##############
        """
        """
        Récupération de tous les paramètres
        tri             => type de tri sélectionné
        entity_sel      => entité sélectionnée
        start_date      => date de début de recherche (début plage)
        end_date        => date de fin de recherche (fin plage)
        clotured        => type d'utilisation de la plage de date
        download
        tri_filters_aff 
        """
        all_params = recup_all_params(request)
        "Récupération du cache_name"
        cache_name = gen_cache_name(all_params,"d_moy_emp")
        "dans le cas où le tri est par affiliation, il faut supprimer le dernier élément du tri_filters_aff, utilisé pour le cache_name"
        if (all_params["tri"] == 0):
            all_params["tri_filters_aff"].pop()

        """
        ############# Traitement de la demande (requête) ##############
        """
        "Dans le cas où une requête identique est stockée dans le cache on la récupère et on la renvoie directement"
        stat = cache.get(cache_name, None)
        if (stat is None):
            """
            dictionnaire de résultats
                chaque clé correspond à un objet de tri, du tri souhaité
                    et est liée à un tableau :
                        en [0] => contient un tableau avec les informations sur l'objet de tri
                        en [1] => la statistique souhaitée
            """
            stat = []
            base_loan = gen_base_loan(all_params)
            
            if (all_params["tri"] == 0):
                stat = trait_global(all_params,base_loan,"d_moy_emp")

            elif ([1,2,3].count(all_params["tri"]) > 0):
                stat = trait_global(all_params,base_loan,"d_moy_emp")

            "Tri des valeurs par ordre décroissant"
            stat = sorted(stat, key=lambda item:item[1],reverse=True)
            "Création d'un cache"
            cache.set(cache_name,stat,900)
        "On envoie une réponse"
        if (all_params["download"] != -1):
            try:
                if (all_params["download"] == 0):
                    "Création du tableau 'params_text'"
                    params_text = gen_params_text(all_params)
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],1,params_text,request.user),status=status.HTTP_200_OK)
                else:
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],1),status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(paginate_by(stat,request.query_params.get('offset'),request.query_params.get('reverse_order'),request.query_params.get('limit')),status=status.HTTP_200_OK)


    "###################### Traitement d'une demande de statistique de type Fréquence d'Emprunt ######################"
    @action(methods=['get'], detail=False)
    def freq_emp(self, request):
        """
        ############# Traitement des paramètres de la requête ##############
        """
        """
        Récupération de tous les paramètres
        tri             => type de tri sélectionné
        entity_sel      => entité sélectionnée
        start_date      => date de début de recherche (début plage)
        end_date        => date de fin de recherche (fin plage)
        clotured        => type d'utilisation de la plage de date
        download
        tri_filters_aff 
        """
        all_params = recup_all_params(request)
        "Récupération du cache_name"
        cache_name = gen_cache_name(all_params,"freq_emp")
        "dans le cas où le tri est par affiliation, il faut supprimer le dernier élément du tri_filters_aff, utilisé pour le cache_name"
        if (all_params["tri"] == 0):
            all_params["tri_filters_aff"].pop()

        """
        Statistique de type Fréquence d'emprunt
            => Cas spécial : on regarde le paramètre filter_freq
        """
        tri_filter_freq = request.query_params.get('filter_freq')
        "Dans les cas incorrects, on initialise à 0 soit la valeur par défaut"
        if (tri_filter_freq is None or tri_filter_freq == ""):
            tri_filter_freq = 0
            'return Response("paramètre filter_freq est null ou inexistant",status=status.HTTP_400_BAD_REQUEST)'
        else:
            try:
                tri_filter_freq = int(tri_filter_freq)
                if (tri_filter_freq < 0 or tri_filter_freq > 2):
                    tri_filter_freq = 0
                    'return Response("paramètre filter_freq n appartient pas à [0,2]",status=status.HTTP_400_BAD_REQUEST)'
            except:
                tri_filter_freq = 0
                'return Response("paramètre filter_freq n est pas un entier",status=status.HTTP_400_BAD_REQUEST)'
        cache_name += 'ff' + str(tri_filter_freq)

        """
        ############# Traitement de la demande (requête) ##############
        """
        "Dans le cas où une requête identique est stockée dans le cache on la récupère et on la renvoie directement"
        stat = cache.get(cache_name, None)
        if (stat is None):
            """
            dictionnaire de résultats
                chaque clé correspond à un objet de tri, du tri souhaité
                    et est liée à un tableau :
                        en [0] => contient un tableau avec les informations sur l'objet de tri
                        en [1] => la statistique souhaitée
            """
            stat = []
            base_loan = gen_base_loan(all_params)

            if (all_params["tri"] == 0):
                stat = trait_global(all_params,base_loan,"freq_emp",tri_filter_freq)

            elif ([1,2,3].count(all_params["tri"]) > 0):
                stat = trait_global(all_params,base_loan,"freq_emp")
            
            "Tri des valeurs par ordre décroissant"
            stat = sorted(stat, key=lambda item:item[1],reverse=True)
            "Création d'un cache"
            cache.set(cache_name,stat,900)
        "On envoie une réponse"
        if (all_params["download"] != -1):
            try:
                if (all_params["download"] == 0):
                    "Création du tableau 'params_text'"
                    params_text = gen_params_text(all_params)
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],2,params_text,request.user),status=status.HTTP_200_OK)
                else:
                    return Response(prepareToDownload(stat,all_params["download"],all_params["tri"],2),status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(paginate_by(stat,request.query_params.get('offset'),request.query_params.get('reverse_order'),request.query_params.get('limit')),status=status.HTTP_200_OK)