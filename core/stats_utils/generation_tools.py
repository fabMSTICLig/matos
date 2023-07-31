# -*- coding: utf-8 -*-
from django.db.models import Q
from ..models import (
    Entity,
    Loan,)

"""
Fonction qui prend en paramètre toutes les données nécessaires à la création d'un nom de cache cohérent
    => ces données requises sont tous les paramètres d'une requête HTTP de statistiques
    => type correspond au type de stat

WARN : Aucune protection sur les paramètres, une erreur surviendra si l'un d'eux est vide
        => ce problème ne survient pas dans l'utilisation d'origine
"""
def gen_cache_name(all_params,type_s):
    "création du cache name avec le début de sa valeur"
    cache_name = all_params["entity_sel"].name + "sd" + str(all_params["start_date"].day) + str(all_params["start_date"].month) + str(all_params["start_date"].year) + "ed" + str(all_params["end_date"].day) + str(all_params["end_date"].month) + str(all_params["end_date"].year) + "clot" + str(all_params["clotured"])
    "si tri par affiliation alors besoins des filtres => cache différent"
    if (all_params["tri"]==0):
        "étape nécessaire pour différencier les caches avec et sans filtres"
        cache_name += "filAff" + all_params["tri_filters_aff"][-1]
    else:
        "sinon, la recherche est sans filtre => le cache retient également cet élément"
        cache_name += 'noFilters'

    "finalisation création du cache_name"
    if (all_params["tri"] == 0):
        cache_name = type_s + "Aff" + cache_name
    elif (all_params["tri"] == 1):
        cache_name = type_s + "User" + cache_name
    elif (all_params["tri"] == 2):
        cache_name = type_s + "Mat" + cache_name
    elif (all_params["tri"] == 3):
        cache_name = type_s + "Tag" + cache_name

    return cache_name

"""
Fonction qui prend en paramètre tous les paramètres d'une requête HTTP de statistiques 
    pour retourner un tableau de chaîne représentant l'affichage de chacun de ces paramètres dans un fichier PDF

WARN : Aucune protection sur les paramètres, une erreur surviendra si l'un d'eux est vide
        => ce problème ne survient pas dans l'utilisation d'origine
"""
def gen_params_text(all_params):
    "Création du params_text"
    params_text = []
    params_text.append("Entité analysée pour la statistique : " + Entity.objects.get(pk = all_params["entity_sel"].pk).name)
    params_text.append("Date de départ de la recherche : " + str(all_params["start_date"].day) + "/" + str(all_params["start_date"].month) + "/" + str(all_params["start_date"].year))
    params_text.append("Date de fin de la recherche : " + str(all_params["end_date"].day) + "/" + str(all_params["end_date"].month) + "/" + str(all_params["end_date"].year))
    if (all_params["clotured"] == 0):
        params_text.append("Plage de dates utilisée selon la règle : prêts dont date de retour (fin/rendu) comprise dans la plage définie")
    elif (all_params["clotured"] == 1):
        params_text.append("Plage de dates utilisée selon la règle : prêts dont date de de sortie (début) comprise dans la plage définie")
    else:
        params_text.append("Plage de dates utilisée selon la règle : prêts dont dates de début ET de fin comprises dans la plage définie")
    "finalisation création du params_text"
    if (all_params["tri"] == 0):
        params_text.insert(0,"Paramètres de la statistique :")
        "Création d'une chaîne contenant le nom des filtres"
        temp = "filtres : "
        for i in range(len(all_params["tri_filters_aff"])):
            temp += all_params["tri_filters_aff"][i] + ', '
        params_text.insert(1,"Statistique calculée : nombre d'emprunts pour chaque affiliation\n\t" + temp)
    elif (all_params["tri"] == 1):
        params_text.insert(0,"Paramètres de la statistique :")
        params_text.insert(1,"Statistique calculée : nombre d'emprunts pour chaque utilisateur")
    elif (all_params["tri"] == 2):
        params_text.insert(0,"Paramètres de la statistique :")
        params_text.insert(1,"Statistique calculée : nombre d'emprunts pour chaque objet/matériel (génériques et spécifiques)")
    elif (all_params["tri"] == 3):
        params_text.insert(0,"Paramètres de la statistique :")
        params_text.insert(1,"Statistique calculée : nombre d'emprunts pour chaque tag")

    return params_text

"Fonction qui génère (récupère et filtre) la base de prêt utilisé par le calcul statistique selon les paramètres de la requête"
def gen_base_loan(all_params):
    "base de prêts correspondant à l'entité sélectionnée et au status 'accepté' pour les prêts"
    base_loan = Loan.objects.filter(entity = all_params["entity_sel"]).filter(status = 3)
    "filtrage de la base de prêts avec les dates souhaitées"
    if (all_params["clotured"] == 0):
        base_loan = base_loan.filter(return_date__gte = all_params["start_date"])
        base_loan = base_loan.filter(return_date__lte = all_params["end_date"])
    elif (all_params["clotured"] == 1) :
        base_loan = base_loan.filter(checkout_date__gte = all_params["start_date"])
        base_loan = base_loan.filter(checkout_date__lte = all_params["end_date"])
    else:
        base_loan = base_loan.filter(Q(checkout_date__gte = all_params["start_date"]) & Q(return_date__gte = all_params["start_date"]))
        base_loan = base_loan.filter(Q(checkout_date__lte = all_params["end_date"]) & Q(return_date__lte = all_params["end_date"]))

    return base_loan

"Fonction qui génère les données utiles pour un utilisateur (dans le tri par utilisateur)"
def gen_user_data(user):
    "création d'un tableau avec les données intéressantes de l'utilisateur par rapport aux statistiques"
    temp = [user.first_name,user.last_name]
    "récupération de toutes les affiliations de l'utilisateur"
    temp_aff = ""
    for user_aff in user.affiliations.values():
        if (temp_aff == ""):
            temp_aff = user_aff["name"]
        else:
            temp_aff += ', ' + user_aff["name"]
    temp.append(temp_aff)

    return temp