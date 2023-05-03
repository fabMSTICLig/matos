# -*- coding: utf-8 -*-
from datetime import date

from .models import (
    Entity,
    Affiliation,
    Tag,
    SpecificMaterial,
    SpecificMaterialInstance,
    GenericMaterial,
    Loan,
    LoanGenericItem)

import json

"""
Récupération de tous les prêts anonymisés
"""
def anonymous_loans(entity_select):
    file = open("./archives/archive" + str(entity_select.pk) + ".json","a+")
    file.seek(0)
    temp = file.read()
    if (temp == ""):
        file.close()
        return "Aucun fichier d'archive pour votre entité n'est disponible"
    else:
        file.close()
        return temp
    
def create_archives(date):
    for ent in Entity.objects.all():
        "Tableau des prêts"
        loans = []
        "Récupération des prêts concernant l'entité souhaité"
        base = Loan.objects.filter(entity = ent, checkout_date__lt = date)
        "Parcours de tous les prêts"
        index = 1
        global_gen_mat = []
        global_spe_mat = []
        global_aff = []
        for l in base:
            temp_spe_mat = []
            for mat in l.specific_materials.all():
                temp_spe_mat.append(mat.pk)
                if (global_spe_mat.count(mat.pk) == 0):
                    global_spe_mat.append(mat.pk)
            temp_gen_mat = []
            for mat in l.generic_materials.all():
                temp_gen_mat.append(mat.pk)
                if (global_gen_mat.count(mat.pk) == 0):
                    global_gen_mat.append(mat.pk)
            if (l.affiliation != None):
                aff = l.affiliation.pk
                if (global_aff.count(l.affiliation.pk) == 0):
                    global_aff.append(l.affiliation.pk)
            else:
                aff = None
            if (l.parent != None):
                par = l.parent.pk
            else:
                par = None
            temp_line = {
                "num":index,
                "id":l.pk,
                "status":l.status,
                "checkout_date":str(l.checkout_date),
                "due_date":str(l.due_date),
                "return_date":str(l.return_date),
                "entity":l.entity.name,
                "affiliation":aff,
                "material_gen":temp_gen_mat,
                "material_spe":temp_spe_mat,
                "parent_id":par
            }
            loans.append(temp_line)

        global_tags = []
        "tableau des matériaux génériques"
        mat_g = []
        "Récupération des matériaux génériques"
        base = GenericMaterial.objects.filter(pk__in = global_gen_mat)
        for gm in base:
            temp_tags = []
            for tag in gm.tags.all():
                temp_tags.append(tag.pk)
                if (global_tags.count(tag.pk) == 0):
                    global_tags.append(tag.pk)

            temp_line = {
                "name":gm.name,
                "id":gm.pk,
                "ref_int":gm.ref_int,
                "ref_man":gm.ref_man,
                "localisation":gm.localisation,
                "description":gm.description,
                "tags":temp_tags,
                "active":gm.active,
                "quantity":gm.quantity
            }
            mat_g.append(temp_line)

        "tableau des instances de matériaux spécifiques"
        mat_s_inst = []
        mat_s_iid = []
        "Récupération des instances de matériaux spécifiques"
        base = SpecificMaterialInstance.objects.filter(pk__in = global_spe_mat)
        for sm_inst in base:
            if (mat_s_iid.count(sm_inst.model.pk) == 0):
                mat_s_iid.append(sm_inst.model.pk)
            temp_line = {
                "name":sm_inst.name,
                "id":sm_inst.pk,
                "serial_num":sm_inst.serial_num,
                "description":sm_inst.description,
                "active":sm_inst.active,
                "model_id":sm_inst.model.pk
            }
            mat_s_inst.append(temp_line)

        "tableau des matériaux spécifiques"
        mat_s = []
        "Récupération des matériaux spécifiques"
        base = SpecificMaterial.objects.filter(pk__in = mat_s_iid)
        for sm in base:
            temp_tags = []
            for tag in sm.tags.all():
                temp_tags.append(tag.pk)
                if (global_tags.count(tag.pk) == 0):
                    global_tags.append(tag.pk)

            temp_instances = []
            for inst in sm.instances.all():
                temp_instances.append(inst.pk)
            temp_line = {
                "name":sm.name,
                "id":sm.pk,
                "ref_int":sm.ref_int,
                "ref_man":sm.ref_man,
                "localisation":sm.localisation,
                "description":sm.description,
                "tags":temp_tags,
                "instances":temp_instances,
                "active":sm.active,
            }
            mat_s.append(temp_line)

        "tableau des tags"
        tags = []
        "Récupération des tags"
        base = Tag.objects.filter(pk__in = global_tags)
        for t in base:
            temp_line = {
                "name":t.name,
                "id":t.pk
            }
            tags.append(temp_line)

        "tableau des affiliations"
        affs = []
        "Récupération des affiliations"
        base = Affiliation.objects.filter(pk__in = global_aff)
        for aff in base:
            temp_line = {
                "name":aff.name,
                "id":aff.pk,
                "type":aff.type
            }
            affs.append(temp_line)

        res = {
            "loan":loans,
            "generic_material":mat_g,
            "specific_material_instance":mat_s_inst,
            "specific_material":mat_s,
            "tag":tags,
            "affiliation":affs
        }

        jsonF = json.JSONEncoder().encode(res)
        "Créer un fichier ici pour sauvegarder le fichier"
        file = open("./archives/archive" + str(ent.pk) + ".json","w")
        file.write(jsonF)
        file.close()

"""
Purge de la base de données selon les critères RGPD
"""
def purge_all():
    try:
        "Deux phase, purge des prêts de +1 an puis purge des utilisateurs n'ayant pas emprunté depuis 2 ans"
        end_date_purge = date((date.today().year-1),1,1)
        create_archives(end_date_purge)
        Loan.objects.filter(checkout_date__lt = end_date_purge).delete()
        return "Purge Effectuée et fichiers d'archive créés"
    except:
        """
        La purge n'est pas effectuée si les archives ne sont pas construites
            et
        Les archives sont construites si la purge échoue
        """
        return "Erreur survenue pendant la purge ou la création des fichiers d'archives"