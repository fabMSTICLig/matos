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
from datetime import timedelta
from django.db.models import Q, Sum
from ..models import (
    Entity,
    Affiliation,
    Tag,
    SpecificMaterial,
    SpecificMaterialInstance,
    GenericMaterial,
    Loan,
    LoanGenericItem)

import os
import json
from reportlab.lib.pagesizes import A4 #Importations
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph

"""
utilisé pour calculer la statistique de la freq_emp
"""
def calc_freq(base_loan, tri_filter_freq):
    res = base_loan.count()
    if (tri_filter_freq == 0):
        return res
    elif (tri_filter_freq == 1):
        if (res != 0):
            return res
    else:
        if (res == 0):
            return res
    return None

"""
utilisé pour calculer la statistique du nb_emp
"""
def calc_nb(base_loan, tag = None, mat = None):
    "variable correspondant au compte de tous les éléments présents dans tous les prêts relatifs à une affiliation"
    res = 0
    """
    calcul statistique : effectué sur chaque objet de prêt
        => pour obtenir le nombre total d'emprunts (à l'unité)
    """
    for loan in base_loan:
        "ajout du total de matériels spécifiques empruntés"
        "parcours des matériels génériques pour prendre en compte leur quantité"
        if (tag is not None):
            temp_q = LoanGenericItem.objects.filter(Q(loan__pk = loan.pk) & Q(material__tags__pk = tag.pk)).aggregate(Sum("quantity"))['quantity__sum']
        elif (mat is not None):
            temp_q = LoanGenericItem.objects.filter(Q(loan__pk = loan.pk) & Q(material__pk = mat.pk)).aggregate(Sum("quantity"))['quantity__sum']
        else:
            res += loan.specific_materials.count()
            temp_q = LoanGenericItem.objects.filter(loan__pk = loan.pk).aggregate(Sum("quantity"))['quantity__sum']
        if (temp_q is not None):
            res += temp_q
    return res

"""
Calcul d'une durée moyenne de prêt grâce à 3 paramètres :
    type_d => string correspond à un type de tri, utilisé pour la récupération de la base de prêts servant aux calculs
    data => Objet correspondant à la donnée recherchée, utilisé pour la récupération de la base de prêts servant aux calculs
    base_loan => BaseManager[Loan] servant de base à la recherche, c'est une filtration du total des prêts

return => if a duration exist : number of days (int)
          else : 0 (int)

WARNING => la fonction ne prend pas en charge les cas où les paramètres type_d et data ne sont pas du même type, 
        cela peut conduire à des erreurs mais dans un cas normal, cela provoquera le renvoie de :
            0 (int)
"""
def calc_duree_moy(type_d,data,base_loan):
    moy = None
    prets = []
    
    "Récupération des données requises grâce à la data et au type_d donnés"
    if (type_d == "aff"):
        prets = base_loan.filter(affiliation__pk=data.pk)
    elif (type_d == "user"):
        prets = base_loan.filter(user__pk=data.pk)
    elif (type_d == "gen_obj"):
        prets = base_loan.filter(generic_materials__pk=data.pk)
    elif (type_d == "spec_obj"):
        prets = base_loan.filter(specific_materials__pk=data.pk)
    elif (type_d == "tag"):
        prets = base_loan.filter(Q(generic_materials__tags__pk = data.pk) | Q(specific_materials__model__tags__pk = data.pk))
    elif (type_d == "Naff"):
        prets = base_loan.filter(affiliation = data)
    else:
        raise Exception("wrong params for calc_duree_moy(type_d,data,base_loan)")

    "Parcours des prêts"
    for loan_act in prets:
        """
        si il y a une date de retour 
            => pas de durée de prêt si il n'est pas terminé
        """
        if (loan_act.return_date is not None):
            """
            dans le cas où aucune durée n'est encore enregistrée
                => on assigne la première durée
            sinon
                => on ajoute la nouvelle durée à l'ancienne
            """
            if (moy is None):
                "différence de jours entre date de retour et date de prêt"
                "+ 1 jour pour le premier jour"
                moy = (loan_act.return_date - loan_act.checkout_date) + timedelta(1)
            else:
                "différence de jours entre date de retour et date de prêt"
                "+ 1 jour pour le premier jour"
                moy += (loan_act.return_date - loan_act.checkout_date) + timedelta(1)
    
    """
    si aucune durée valide trouvée pendant le parcours des prêts
        => assigner -1
    sinon
        => calcul de la moyenne de durée
    """
    if (moy is not None):
        moy = (moy/prets.count()).days
    else:
        """
        alors moy is None, assigne 0
            => provoque message frontend => 'Aucune durée de prêt'
        """
        moy = 0

    return moy

"""
Fonction permettant la pagination d'une donnée grâce à 3 paramètres :
    data => [ [ [] , [] ],[ [] , [] ] ] tableau de tableaux de tableaux (par rapport aux statistiques, correspond à la forme d'un élément de retour, variable 'stat')
    offset => élément de départ de la page
    reverse => inverse l'ordre des pages, la offset 0 avec reverse = True, renverra la dernière page
    limit => integer, nombre d'éléments par page (par défaut = 100)
"""
def paginate_by(data,offset = 0,reverse = False,limit = 100):
    "le paramètre offset peut recevoir un paramètre de requête qui n'existe pas forcément => par défaut = 0"
    if (offset is None or offset == ""):
        offset = 0
    try:
        "transformation en entier, sert également à tester si offset est un entier"
        offset = int(offset)
    except:
        'raise Exception("parameter offset is not an integer")'
        return 0
    
    "le paramètre reverse peut recevoir un paramètre de requête qui peut avoir plusieurs forme ou ne pas exister"
    "existe => True"
    "n'existe pas ou vide => False"
    if (reverse is None or reverse == ""):
        reverse = False
    try:
        reverse = bool(reverse)
    except:
        'raise Exception("parameter reverse is not a boolean") => normalement impossible car une chaîne non vide renvoie true'
        return False
    
    "le paramètre limit peut recevoir un paramètre de requête qui peut avoir plusieurs forme ou ne pas exister"
    if (limit is None or limit == ""):
        "=> par défaut = 100"
        limit = 100
    try:
        "transformation en entier, sert également à tester si limit est un entier"
        limit = int(limit)
    except:
        'raise Exception("parameter limit is not an integer")'
        limit = 100

    """
    test que offset soit supérieur ou égal à 0
        ET
    que limit soit supérieur ou égal à 1
    """
    if (offset >= 0 and limit >= 1):
        start_elem = offset
        end_elem = start_elem + limit
        if (end_elem >= len(data)):
            end_elem = len(data)
        if (start_elem >= len(data)):
            "dans le cas où l'élément de départ n'est pas dans l'intervalle d'index de la data, on ne peut pas démarrer => pas de page"
            return None
        "Si inversion demandée"
        if (reverse):
            "inversion de l'ordre des éléments"
            data.reverse()
    else:
        return None
    "création du tableau contenant les données de la page souhaitée"
    page_data = data[start_elem:end_elem]
    "longueur total utilisé par le front pour déterminer le nombre de pages total"
    page_data.append(len(data))
    return page_data

"""
Fonction ayant pour but de préparer une donnée 'data' calculée pour une statistique
pour un téléchargement (return a String) dans un des formats proposés suivants :
    - pdf (0), indisponible pour le moment => in development
    - csv (1) => format CSV classique, delimiter = ',' | first line is not title of each column but the first value
    - json (2) => data stringify in JSON format
    - txt (3) => each line is one value of data
nécessite également le type de tri et de statistique
    - type_tri = integer ([0,1,2,3])
    - type_stat = integer ([0,1,2])
un 'params_text' est nécessaire pour les fichiers pdf, c'est pourquoi il possède une valeur par défaut (pour les autres cas)
    => ce paramètre correspond au texte au début du pdf décrivant les paramètres de la recherche
l'utilisateur actuel est également nécessaire sous la dénomination 'user'
    => ce paramètre est utilisé pour décrire le nom que prendre un fichier pdf, encore une fois, il possède une valeur par défaut 
       faciliter l'utilisation de la fonction sur les autres types de fichier n'en ayant pas l'utilité.
"""
def prepareToDownload(data, format, type_tri, type_stat, params_text = "", user = None):
    """
        INFO => les paramètres ne sont pas testés car ils sont envoyés par le code précédent, il est donc induit qu'ils sont valides
        WARN => ces paramètres sont à tester si la fonction doit être utilisé dans un contexte à risque ou si les paramètres sont donnés par un utilisateur

        PS : 'format' est déjà testé lors de l'appel à cette fonction (voir return Response dans views.py), 
             les valeurs possibles sont déjà limitées dans recup_params_tools.py dans la fonction se chargeant de traiter le paramètre HTTP correspondant
    """

    """
    Assignation du nom de la statistique, qui correspond au type de statistique choisi 
        => utilisé notamment pour écrire dans un fichier la statistique en question
    """
    if (type_stat == 1):
        name_stat = "Durée moy emprunts (en jours)"
    elif (type_stat == 2):
        name_stat = "Fréquence emprunts"
    else:
        name_stat = "Nb emprunts"

    "dictionnaire prédéfinie => seule la ligne correspondant au type de tri en paramètre sera utilisée"
    columns = {
        'aff':["Affiliation",name_stat],
        'object':["Nom","Référence Interne","Référence Fabricant","Nom Instance","Numéro de série Instance",name_stat],
        'tag':["Tag",name_stat]
    }
    """
    si le format souhaité est le PDF (0), l'utilisateur étant nécessaire pour créer le fichier, 
    son existence est testée mais il n'est pas censé pouvoir être Null si le format sélectionné est le pdf 
        => (assuré par le code appelant la fonction et les obligations d'authentification de l'application)
    """
    if (format == 0 and user != None and type_tri != 1):
        "in PDF"
        "tableau des éléments de notre pdf, contient les éléments qui seront écrits dans le pdf"
        elements = []

        "titre du pdf"
        title_style = PS(name = 'Heading1',fontSize = 20, spaceAfter = 24, alignment = 1)
        elements.append(Paragraph("<b><u>Récapitulatif Statistique</u></b>",title_style))

        "informations (style et valeur) sur le titre de l'encart décrivant les paramètres de statistique"
        params_h_style = PS(name = 'para1', fontsize = 12, spaceAfter = 10, spaceBefore = 20, fontSize = 14)
        temp_str = "<u>" + params_text.pop(0) + "</u>"
        elements.append(Paragraph(temp_str,params_h_style))

        "informations (style et valeurs) sur les paramètres de statistique"
        params_style = PS(name = 'para2', parent=params_h_style, leftIndent = 24, spaceBefore = 0, fontSize = 12)
        for pg in params_text:
            elements.append(Paragraph(pg,params_style))

        "ajout du titre du tableau des données en utilisant le style du titre des paramètres"
        elements.append(Paragraph("<u>Tableau de données :</u>",params_h_style))

        "sélection de la ligne du tri entré en paramètre"
        if (type_tri == 0):
            tri = columns["aff"]
        elif (type_tri == 2):
            tri = columns["object"]
        else:
            tri = columns["tag"]
        
        "création du fichier pdf vierge"
        pdf_file = SimpleDocTemplate("recap-statistiques_" + name_stat + "_user-"+ str(user.pk) + '_' + user.first_name + '-' + user.last_name +".pdf",pagesize=A4,title="Récapitulatif Statistique demandé par "+user.first_name)

        """
        Traitement spécifique de 'data' pour diminuer le nombre de sous-liste et équilibrer la profondeur 
            => transformer le tableau de tableaux de tableaux en tableau de tableaux
        """
        data_to_PDF = []
        for line in data:
            "tableau de données temporaire pour stocker les données post-traitement"
            tempD = []
            "parcours de chaque donnée non statistique"
            for data_line in line[0]:
                """
                Si les données (hors données de la statistique) sont plus nombreuses que 3, le tableau aura plus de 4 colonnes
                    => il est donc nécessaire de mettre les string des données sur plusieurs lignes pour économiser de l'espace

                WARN => Si les données se trouvent être plus nombreuses qu'à l'origine, veillez à diminuer la valeur de la variable nb_char
                        => cette valeur représente le nombre de caractères maximum d'une ligne
                        => la valeur utilisée réellement est égale à nb_char + 1 (les intervalles en python exclus la valeur de fin)
                """
                nb_char = 14
                if (len(line[0]) > 3):
                    if data_line is None:
                        "cas où la donnée est null, la chaîne doit valoir être une chaîne vide"
                        temp_str = ""
                    else:
                        "cas où la donnée porte une valeur (toutes les valeurs traitées doivent être des String)"

                        """
                        line_str : copie de data_line, fondamentalement inutile car elle n'est jamais modifiée => permet de distinguer ce qu'on manipule
                        temp_str : chaîne temporaire, correspond à la chaîne initiale avec des retours à la ligne
                        index_deb : correspond à l'index du début du morceau de chaîne analysée (la chaîne est analysée par tranche de 'nb_char' éléments)
                        reste_a_parc : entier correspondant au nombre d'éléments restant à analyser 
                            WARN => (équivalent d'un len, ne correspond pas à l'indice du dernier élément)
                        """
                        line_str = data_line
                        temp_str = None
                        index_deb = 0
                        reste_a_parc = len(line_str)
                        "on répète l'opération de découpage tant que le nombre d'éléments à parcourir est plus grand que 'nb_char'"
                        while (reste_a_parc > nb_char):
                            "portée d'analyse"
                            range_i = index_deb + (nb_char+1)
                            """
                            Reset index, lorsque le morceau après le premier ne contient pas d'espace, de tiret '-' ou de parenthèse ouvrante '('
                                => initialise également la variable
                            """
                            index = 0
                            "parcours des éléments à analyser"
                            for i in range(index_deb,range_i):
                                "si un élément est un espace, un tiret '-' ou une parenthèse ouvrante '(', on récupère son indice"
                                if (line_str[i] == ' ' or line_str[i] == '-' or line_str[i] == '('):
                                    """
                                    indice assigné à index => correspond au dernier emplacement de découpage possible
                                        => une assignation comme cela permet de ne garder que le dernier indice, le plus proche des 'nb_char' max
                                    """
                                    index = i
                            "si on a pas trouvé d'emplacement de découpage"
                            "sinon => on a trouvé"
                            if (index == 0):
                                "si temp_str non vide"
                                if (temp_str is not None):
                                    """
                                    on ajoute un retour à la ligne puis le morceau de chaîne correspondant à l'analyse effectuée
                                       => dans ce cas, on coupe après 'nb_char' car aucun meilleur emplacement n'a été trouvé
                                    """
                                    temp_str += "\n" + line_str[index_deb:(nb_char+1)]
                                else:
                                    """
                                    1er découpage => on définit 'temp_str' comme le morceau de chaîne correspondant à l'analyse effectuée
                                       => dans ce cas, on coupe après 'nb_char' car aucun meilleur emplacement n'a été trouvé
                                    """
                                    temp_str = line_str[:(nb_char+1)]
                                "on retire au reste d'éléments à analyser le nombre d'éléments analysé"
                                reste_a_parc = reste_a_parc - (nb_char+1)
                                "on modifie le point de départ pour la prochaine analyse, ajout du nombre d'éléments analysé"
                                index_deb += (nb_char+1)
                            else:
                                "si temp_str non vide"
                                if (temp_str is not None):
                                    """
                                    on ajoute un retour à la ligne puis le morceau de chaîne correspondant au découpage déterminé
                                       => dans ce cas, on coupe après 'index' car c'est le meilleur emplacement trouvé
                                    """
                                    temp_str += "\n" + line_str[index_deb:index+1]
                                else:
                                    """
                                    1er découpage => on définit 'temp_str' comme le morceau de chaîne correspondant au découpage déterminé
                                       => dans ce cas, on coupe après 'index' car c'est le meilleur emplacement trouvé
                                    """
                                    temp_str = line_str[:index + 1]
                                    "on retire au reste d'éléments à analyser le nombre d'éléments avant le point de découpe (le point de découpe est inclus)"
                                reste_a_parc = reste_a_parc - (index - index_deb) - 1
                                "on modifie le point de départ pour la prochaine analyse, ajout du nombre d'éléments analysé"
                                index_deb = index + 1
                        "si une chaîne divisée a été créée"
                        if (temp_str is not None):
                            "Ajout du dernier morceau"
                            temp_str += "\n" + line_str[index_deb:]
                        else:
                            """
                            sinon, c'est que la chaîne d'origine fait moins de 'nb_char' caractères
                                => on passe donc la chaîne d'origine dans sa totalité à la chaîne temporaire => commodité pour ne conserver un unique append en fin de bloc
                            """
                            temp_str = line_str
                    "Ajout de la donnée au tableau de données, dans le cas où le nombre de colonnes nécessitait un traitement de la donnée"
                    tempD.append(temp_str)
                else:
                    "Ajout de la donnée au tableau de donnée, dans le cas où aucun traitement n'était nécessaire à cause du nombre de colonnes"
                    tempD.append(data_line)
            "donnée statistique transformé en string (aucun test n'est effectué)  WARN => si des données non stringifiable sont ajoutées dans les data veillez à ajouter un try/except"
            tempD.append(str(line[1]))
            "ajout du tableau des données traitées au tableau définitif"
            data_to_PDF.append(tempD)
        "insertion de la ligne correspondante au nom de chaque donnée du tableau"
        data_to_PDF.insert(0,tri)

        "Construction d'un objet Table avec notre tableau de données, un objet Table correspond à un tableau écrivable sur un PDF"
        tab = Table(data_to_PDF)
        "Définition du style appliqué au Tableau de notre PDF"
        tab.setStyle([('TEXTCOLOR',(0,0),(len(tri),0),colors.blue),
                        ('BACKGROUND',(0,0),(len(tri),0),colors.lightgrey),
                        ('INNERGRID', (0,0), (len(tri),len(data_to_PDF)), 0.25, colors.black),
                        ('ALIGN',(0,0), (len(tri),len(data_to_PDF)),'CENTER')])
        "ajout de notre tableau aux éléments contenus dans le pdf"
        elements.append(tab)
        "Construction du fichier pdf grâce au tableau de tous les éléments"
        pdf_file.build(elements)
        "ouverture et lecture en format bitBybit du fichier pdf sauvegardé"
        file_to_return = open("./recap-statistiques_" + name_stat + "_user-"+ str(user.pk) + '_' + user.first_name + '-' + user.last_name +".pdf","rb").read()
        "décodage du fichier avec l'encodage pdf utilisé"
        file_to_return = file_to_return.decode("ISO8859-1")
        "suppression du fichier sur le disque du serveur"
        os.remove("./recap-statistiques_" + name_stat + "_user-"+ str(user.pk) + '_' + user.first_name + '-' + user.last_name +".pdf")
        "retour du fichier sous format String décodé pour envoie par Réponse HTTP"
        return file_to_return
    elif (format == 1 and type_tri != 1):
        """
        Format sélectionné = 1 => CSV
        INFO : la ligne répertoriant les noms des colonnes est générée côté frontend
        """

        "chaîne correspondant au fichier CSV"
        csv_file = ""
        "parcours de chaque groupe de donnée => TABLEAU contenant un tableau de données non statistiques et un tableau contenant la donnée statistique"
        for d in data:
            """
            données propres au tri par utilisateur, il est nécessaire de passer par un traitement spéciale
                car la 3ème donnée est une chaîne qui contient chaque affiliation de l'utilisateur séparée par une virgule,
                cela pose donc problème pour le format CSV, on remplace donc ces virgules par des esperluettes '&'
            """
            if (type_tri == 1):
                csv_file += str(d[0][0]) + ","
                csv_file += str(d[0][1]) + ","
                csv_file += d[0][2].replace(", "," & ") + ","
            else:
                "Pour n'importe quel autre type de tri, on parcourt chaque donnée non statistique"
                for sd in d[0]:
                    "on ajoute la donnée parcouru à la chaîne du fichier puis on y accole une virgule ',' pour respecter le format CSV"
                    csv_file += str(sd) + ","
            "donnée statistique, on ajoute la donnée statistique puis on met un retour chariot pour indiquer le début d'une nouvelle ligne"
            csv_file += str(d[1]) + "\n"
        "une fois toutes les données parcourues, on retourne la chaîne correspondant au fichier CSV"
        return csv_file
    elif (format == 3 and type_tri != 1):
        """
        Format sélectionné = 3 => TXT
        INFO : la ligne répertoriant les noms des colonnes est générée côté frontend, avant la ligne de séparation ci-dessous

        Pour ce format il a été décidé qu'il serait généré comme un CSV à la différence que le séparateur est une ligne verticale '|'
        les données peuvent être théoriquement ouvertes comme un CSV mais il faut penser à changer le séparateur par défaut.
        WARN : la ligne séparant les titres des colonnes, du reste des données décale les colonnes, aussi il est préférable de SUPPRIMER cette ligne
        """
        txt_file = "===================================================================================================\n"
        for d in data:
            "données propres au tri"
            if (type_tri == 1):
                txt_file += str(d[0][0]) + "|"
                txt_file += str(d[0][1]) + "|"
                txt_file += d[0][2].replace(", ",'&') + "|"
            else:
                for sd in d[0]:
                    txt_file += str(sd) + "|"
            "valeur de stat"
            txt_file += str(d[1]) + "\n"
        return txt_file
    elif (format == 2 and type_tri != 1):
        """
        Format sélectionné = 2 => JSON
        INFO : l'objet contenant les noms des différentes données est générée côté frontend sous le nom 'order'

        la génération de ce fichier se fait facilement car il suffit d'appeler une fonction python sur le tableau 'data'
        """
        return json.JSONEncoder().encode(data)
    else:
        raise Exception("Wrong Request (! => stats by user cannot be download)")