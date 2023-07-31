# -*- coding: utf-8 -*-
from datetime import date

from ..models import (
    Entity,
    Affiliation,
    Tag,
    SpecificMaterial,
    SpecificMaterialInstance,
    GenericMaterial,
    Loan,
    LoanGenericItem)

"""
Traitement du paramètre standard tri d'une requête de statistiques

#return : 
    tri => valeur paramètre tri de la requête (entier compris dans [0,3])
                        
    Exception => dans le cas où il n'y a pas de paramètre tri
                             où le paramètre tri n'est pas un entier
                             où le paramètre tri n'est pas compris entre 0 et 3 inclus
"""
def params_request_tri(req):
    "Récupération du paramètre 'tri'"
    tri = req.query_params.get('tri', None)
    "Si paramètre tri est none c'est anormal et on ne peut pas continuer"
    if (tri is None or tri==""):
        raise Exception("param tri is None or not exist")
    else:
        "tri != None donc transformation en entier"
        try:
            tri = int(tri)
        except:
            "Si tri n'est pas un entier, int() renvoie une erreur qu'on intercepte"
            raise Exception("param tri, is not an integer")
        "tri compris entre 0 et 3 ?"
        if (tri >= 0 and tri <= 3):
            return tri
        else:
            raise Exception("param tri is not in [0,3]")

"""
Traitement du paramètre standard entity_selected d'une requête de statistiques

#return :
    entity_sel => objet de type Entity correspondant à l'entité dont l'utilisateur souhaite obtenir les statistiques

    Exception => dans le cas où le paramètre entity_selected est none ou vide
                             où le paramètre entity_selected n'existe pas parmi les objets Entity
                             où l'utilisateur actuel n'est pas manager de l'Entity sélectionnée
"""
def params_request_entity(req):
    "Récupération du paramètre 'entity_selected'"
    entity_sel = req.query_params.get('entity_selected', None)
    "Récupération de l'utilisateur ayant effectué la requête"
    user = req.user
    "si paramètre est none ou inexistant, on ne peut continuer"
    if (entity_sel is None or entity_sel==""):
        raise Exception("param entity_selected is None or not exist")
    else:
        "entity_sel est une entité existante ?"
        try:
            entity_sel = Entity.objects.get(pk = entity_sel)
            if (entity_sel.managers.contains(user)):
                return entity_sel
            else:
                raise Exception(user.username + " don't have permission to consult stats of this entity")
        except Entity.DoesNotExist:
            raise Exception("param entity_selected is not an existing entity")

"""
Traitement du paramètre optionnel clotured d'une requête de statistiques

return :
    clotured => boolean correspondant à si le calcul doit supprimer ou non les prêts non cloturés
        True = prend en compte les prêts non cloturés
        False = ne prend pas en compte les prêts non cloturés
"""        
def params_request_clotured(req):
    "récupération du paramètre"
    clotured = req.query_params.get('clotured', None)
    if (clotured is None or clotured == ""):
        return 0
    else :
        try:
            clotured = int(clotured)
            if (clotured <= 2 and clotured >= 0):
                return clotured
            else:
                return clotured
        except:
            return 0
        
"""
Récupération et validation d'un paramètre optionnel de date

prend une requête en paramètre pour permettre la consultation des paramètres 
de cette requête et notamment l'accès au paramètre 'start_d' ou 'end_d'

prend également une chaîne de caractères correspondant au paramètre souhaité

return => starting date (date) or ending date (date) (determinate by 'param')
          or an Exception
"""
def params_request_d(req, param):
    d = req.query_params.get(param, None)

    if (d is None or d == ""):
        raise Exception("param " + param + " is None or not exist")
    else:
        d = d.split('-')
        if (len(d) != 3):
            raise Exception("incorrect number of arguments in param " + param + " or wrong separator")
        else:
            for i in range(3):
                "transformation en entiers des chaînes stockées"
                try:
                    d[i] = int(d[i])
                except:
                    raise Exception("arguments are not integers in " + param)
                
            "transformation en date du tableau d"
            try:
                d_date = date(d[0],d[1],d[2])
            except:
                raise Exception("incorrect arguments to make a date in " + param)
    return d_date

"""
Récupération et validation d'un paramètre de téléchargement

prend une requête en paramètre pour permettre la consultation des paramètres 
de cette requête et notamment l'accès au paramètre 'download'

return => integer in [-1,0,1,2,3]
"""
def params_request_dl(req):
    para = req.query_params.get("download", None)
    if (para is None or para == ""):
        return -1
    elif (para == "pdf"):
        return 0
    elif (para == "csv"):
        return 1
    elif (para == "txt"):
        return 3
    elif (para == "json"):
        return 2
    else:
        return -1
    
"""
Récupération et validation du paramètre de filtre par affiliation

prend une requête en paramètre pour permettre la consultation des paramètres 
de cette requête et notamment l'accès au paramètre 'filters_aff'

return => [] array with : Affiliation.TYPE_AFFILIATION (string) and one string of affiliation's id (string)
          #can be empty

          exemple : ['Labo','Ecole','Recherche','014']
"""
def set_tri_filters(req):
    "part of cache name => string of affiliation's id"
    ids = ''
    "Récupération du paramètre"
    tri_filters_aff = req.query_params.get('filters_aff')
    "Dans le cas, où le paramètre filters_aff est vide, on initialise à toutes les valeurs possibles"
    if (tri_filters_aff is None or tri_filters_aff == ""):
        tab_filters_aff = []
        "parcours de tous les types d'affiliations pour les ajouter au tableau de retour => par défaut tous les types doivent être retournés"
        for type in Affiliation.TYPE_AFFILIATION:
            tab_filters_aff.append(type[0])
        "Naff ou Non affilié, n'est pas un type donc il faut le rajouter à la main"
        tab_filters_aff.append("Naff")
        "ids = '012345Naff'"
        tab_filters_aff.append('012345Naff')
        return tab_filters_aff
    else:
        """ 
    Si paramètre filters_aff n'est pas none et qu'il contient au moins une information
    INFO : les tests d'intervalles pour les valeurs sont effectués à la fin
        """
        tri_filters_aff = tri_filters_aff.split(',')
        "vérification de valeurs valides"
        "WARNING : ne traite pas le cas de doublons (traité plus tard à l'ajout dans le tableau de retour)"
        for f in tri_filters_aff:
            "Si valeur non présente parmi les possibilités valides alors le filtre est incorrect car une valeur au moins est invalide"
            if (['0','1','2','3','4','5','Naff'].count(f) == 0):
                raise Exception("filtre incorrect, valeur non présente parmi ['0','1','2','3','4','5','Naff']")
                
        "déclaration tableau des types d'affiliation sélectionnés (temporaire)"
        tab_filters_temp = []
        """
        recherche de 0,1,2,3,4 ou 5 dans le tableau des filtres, si présent au moins 1 fois
            => on ajoute au tableau temporaire le type d'affiliation correspondant
            => on ajoute l'id à la chaîne des identifiants
        """
        for i in range(len(Affiliation.TYPE_AFFILIATION)):
            if (tri_filters_aff.count(str(i)) >= 1):
                tab_filters_temp.append(Affiliation.TYPE_AFFILIATION[i][0])
                ids = ids + (str(i))
        """
        recherche de 'Naff' dans le tableau des filtres, si présent au moins 1 fois
            => on ajoute au tableau temporaire le type d'affiliation correspondant
            => on ajoute l'id à la chaîne des identifiants
        """
        if (tri_filters_aff.count("Naff") >= 1):
            tab_filters_temp.append("Naff")
            ids = ids + "Naff"
        "on ajoute au tableau de retour, la chaîne contenant les id des filtres"
        tab_filters_temp.append(ids)
        return tab_filters_temp

"""
Récupération de tous les paramètres d'une requête de statistiques grâce aux fonctions ci-dessus
    INFO : le paramètre de filtre de fréquence n'est pas traité car étant un cas unique ce n'est pas nécessaire de le déplacer ici

prend une requête en paramètre pour permettre la consultation des paramètres et surtout le passage de la requête aux autres fonctions

return => tableau des valeurs des paramètres
"""
def recup_all_params(req):
    "Récupération du paramètre tri de la requête + vérifications"
    try:
        tri = params_request_tri(req)
    except Exception as excep:
        raise Exception(str(excep))
    
    "Récupération du paramètre entity_selected"
    try:
        entity_sel = params_request_entity(req)
    except Exception as excep:
        raise Exception(str(excep))
    
    "Récupération du paramètre start_d de la requête + vérifications"
    try:
        sd = params_request_d(req,'start_d')
    except Exception:
        sd = date.today()
        sd = sd.replace(year=sd.year - 3)

    "Récupération du paramètre end_d de la requête + vérifications"
    try:
        ed = params_request_d(req,'end_d')
    except Exception:
        ed = date.today()
    
    "Récupération du paramètre clotured de la requête + vérifications"
    clot = params_request_clotured(req)

    "Récupération paramètre download"
    dl = params_request_dl(req)

    "si tri par affiliation alors besoins des filtres"
    if (tri==0):
        "Récupération et formatage des filtres"
        try:
            tri_filters_aff = set_tri_filters(req)
        except Exception as excep:
            raise Exception(str(excep))
    else:
        """ 
        Si paramètre tri n'est pas none et qu'il est différent de 0
            => Cas commun : pas besoin des filtres
        """
        tri_filters_aff = None

    "retour de toutes les valeurs récupérées"
    return {"tri":tri,"entity_sel":entity_sel,"start_date":sd,"end_date":ed,"clotured":clot,"download":dl,"tri_filters_aff":tri_filters_aff}