# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from ..models import (
    Entity,
    Affiliation,
    Tag,
    SpecificMaterial,
    SpecificMaterialInstance,
    GenericMaterial,
    Loan,
    LoanGenericItem)

from ..stats_utils.data_tools import *
from .generation_tools import gen_user_data

"""
traitement spécifique pour un tri par affiliation
"""
def trait_spe_aff(base_loan,type_stat,tri_filters_aff,tri_filter_freq):
    "tableau de résulats"
    stat= []
    res = None
    "Chargement des données de tri correspondantes"
    data_tri = Affiliation.objects.all()
    "calcul de la statistique pour chaque objet du tri + ajout au dictionnaire de résultats"
    for aff in data_tri.filter(type__in = tri_filters_aff):
        if (type_stat != "d_moy_emp"):
            "Sélection des prêts selon le tri souhaité"
            base_loan_temp = base_loan.filter(affiliation__pk = aff.pk)
            if (type_stat == "nb_emp"):
                res = calc_nb(base_loan_temp)
            else:
                res = calc_freq(base_loan_temp,tri_filter_freq)
        else:
            try:
                res = calc_duree_moy("aff",aff,base_loan)
            except:
                "peut recevoir une exception en cas d'entrée de mauvais arguments à la fonction calc_duree_moy(type_d,data)"
                res = None
        """
        intégration dans le tableau de résultat de la statistique
            avec les données intéressante sur l'objet de tri
        """
        if (res is not None):
            stat.append([[aff.name],res])
    if ("Naff" == tri_filters_aff[-1]):
        if (type_stat != "d_moy_emp"):
            base_loan_temp = base_loan.filter(affiliation = None)
            if (type_stat == "nb_emp"):
                "variable correspondant au compte de tous les éléments présents dans tous les prêts relatifs à une affiliation"
                res = calc_nb(base_loan_temp)
            else:
                res = calc_freq(base_loan_temp,tri_filter_freq)
        else:
            try:
                res = calc_duree_moy("Naff",None,base_loan)
            except:
                "peut recevoir une exception en cas d'entrée de mauvais arguments à la fonction calc_duree_moy(type_d,data)"
                res = None
        """
        intégration dans le tableau de résultat de la statistique
            avec les données intéressante sur l'objet de tri
        """
        if (res is not None):
            stat.append([["Sans Affiliation"],res])
    return stat

"""
traitement spécifique pour un tri par material
"""
def trait_spe_mat(base_loan,type_stat,tri_filter_freq):
    "tableau de résulats"
    stat= []
    res = None
    "Chargement des données de tri correspondantes"
    data_tri = GenericMaterial.objects.all()
    for gmat in data_tri.all():
        if (type_stat != "d_moy_emp"):
            base_loan_temp = base_loan.filter(generic_materials__pk = gmat.pk)
            if (type_stat == "nb_emp"):
                "variable correspondant au compte de tous les éléments présents dans tous les prêts relatifs à une affiliation"
                res = calc_nb(base_loan_temp,mat=gmat)
            else:
                res = calc_freq(base_loan_temp,tri_filter_freq)
        else:
            try:
                res = calc_duree_moy("gen_obj",gmat,base_loan)
            except:
                "peut recevoir une exception en cas d'entrée de mauvais arguments à la fonction calc_duree_moy(type_d,data)"
                res = None
        if (res is not None):
            stat.append([[gmat.name,gmat.ref_int,gmat.ref_man,"",""],res])

    data_tri = SpecificMaterialInstance.objects.all()
    for smat in data_tri.all():
        if (type_stat != "d_moy_emp"):
            base_loan_temp = base_loan.filter(specific_materials__pk = smat.pk)
            if (type_stat == "nb_emp"):
                "variable correspondant au compte de tous les éléments présents dans tous les prêts relatifs à une affiliation"
                res = base_loan_temp.count()
            else:
                res = calc_freq(base_loan_temp,tri_filter_freq)
        else:
            try:
                res = calc_duree_moy("spec_obj",smat,base_loan)
            except:
                "peut recevoir une exception en cas d'entrée de mauvais arguments à la fonction calc_duree_moy(type_d,data)"
                res = None
        if (res is not None):
            stat.append([[smat.model.name,smat.model.ref_int,smat.model.ref_man,smat.name,smat.serial_num],res])

    return stat

"""
Traitement global pour les tri
"""
def trait_global(all_params,base_loan,type_stat,tri_filter_freq = 0):
    if (all_params["tri"] == 0):
        return trait_spe_aff(base_loan,type_stat,all_params["tri_filters_aff"],tri_filter_freq)
    elif (all_params["tri"] == 2):
        return trait_spe_mat(base_loan,type_stat,tri_filter_freq)
    else:
        "tableau de résulats"
        stat= []
        res = None
        "Chargement des données de tri correspondantes"
        if (all_params["tri"] == 1):
            data_tri = get_user_model().objects.filter(loans__in = base_loan).distinct()
            name_data = "user"
        else:
            data_tri = Tag.objects.all()
            name_data = "tag"
        "calcul de la statistique pour chaque objet du tri + ajout au dictionnaire de résultats"
        for obj in data_tri.all():
            if (type_stat != "d_moy_emp"):
                "Sélection des prêts selon le tri souhaité"
                if (all_params["tri"] == 1):
                    base_loan_temp = base_loan.filter(user__pk = obj.pk)
                else:
                    base_loan_temp = base_loan.filter(Q(generic_materials__tags__pk = obj.pk) | Q(specific_materials__model__tags__pk = obj.pk)).distinct()
                if (type_stat == "nb_emp"):
                    if (all_params["tri"] == 3):
                        res = calc_nb(base_loan_temp,obj)
                    else:
                        res = calc_nb(base_loan_temp)
                else:
                    res = calc_freq(base_loan_temp,tri_filter_freq)
            else:
                try:
                    res = calc_duree_moy(name_data,obj,base_loan)
                except:
                    "peut recevoir une exception en cas d'entrée de mauvais arguments à la fonction calc_duree_moy(type_d,data)"
                    res = None
            """
            intégration dans le tableau de résultat de la statistique
                avec les données intéressante sur l'objet de tri
            """
            if (res is not None):
                if (all_params["tri"] == 1):
                    stat.append([gen_user_data(obj),res])
                else:
                    stat.append([[obj.name],res])
        return stat