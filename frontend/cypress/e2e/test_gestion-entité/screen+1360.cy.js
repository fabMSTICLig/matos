const width = 1360
const height = 960
const dDate = new Date()

describe("Gestion entité - Main", () => {
  beforeEach(() => {
    cy.viewport(width,height)

    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get(".dropdown-item").contains("FabMSTIC").click()
  })

  it('Affichage données', () => {
    // vérification de la présence des informations
    cy.get(".card-header > h3").should("have.text","FabMSTIC")
    cy.get("#markdown").should("contain","Fablab universitaire du campus de Saint Martin d'hères")
    cy.get(".card-body ul > li").should("have.length",2)
    cy.get(".card-body ul > li:first").should("have.text","LIG")
    cy.get(".card-body ul > li:last").should("have.text","FabMSTIC")
    cy.get(".card-body > p > a").should("have.text","fabmstic@univ-grenoble-alpes.fr")
  });

  it('Boutons', () => {
    // vérification du bouton "Gestion Matériels"
    cy.get(".btn").contains("Gestion Matériels").click()
    cy.url().should("contain","/entity/1/materials")

    // retour à la page de gestion de l'entité
    cy.visit("/#/entity/1/")

    // vérification du bouton "Gestion prêts"
    cy.get(".btn").contains("Gestion prêts").click()
    cy.url().should("contain","/entity/1/loans")

    // retour à la page de gestion de l'entité
    cy.visit("/#/entity/1/")

    // vérification du bouton "Statistiques"
    cy.get(".btn").contains("Statistiques").click()
    cy.url().should("contain","/entity/1/stats")

    // retour à la page de gestion de l'entité
    cy.visit("/#/entity/1/")

    // vérification du bouton d'édition (seul bouton circulaire)
    cy.get(".btn-circle").click()
    cy.url().should("contain","/entity/1/edit")
  })
});

describe("Gestion entité - Page Gestion des Matériels", () => {
  beforeEach(() => {
    cy.viewport(width,height)

    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get(".dropdown-item").contains("FabMSTIC").click()
    // clic sur le bouton "Gestion Matériels"
    cy.get(".btn").contains("Gestion Matériels").click()
  });

  it('Bouton Retour', () => {
    // clic sur le bouton de retour (présent sur la page, pas celui par défaut du navigateur)
    cy.get(".card-header .btn-group").contains("Retour").click()
    // vérification du bon retour vers la page précédente
    cy.url().should("contain","/entity/1").and("not.contain","materials")
  });

  it('Bouton Aide', () => {
    // clic sur le bouton aide
    cy.get(".card-header .btn-group button.btn-outline-info").click()
    // vérification de l'affichage de la pop-up + vérification de la présence de mots-clés
    cy.get("#modal-help").should("exist")
    cy.get("#modal-help .modal-header").should("contain","Type de matériel")
    cy.get("#modal-help .modal-body ").should("contain","Spécifique").and("contain","Générique").and("contain","instances").and("contain","matériel")
    // vérification fermeture (bouton OK)
    cy.get("#modal-help .btn").contains("Ok").click()
    cy.get("#modal-help").should("not.exist")

    // vérification second bouton de fermeture (croix)
    cy.get(".card-header .btn-group button.btn-outline-info").click()
    cy.get("#modal-help").should("exist")
    cy.get("#modal-help .modal-header .btn-close").click()
    cy.get("#modal-help").should("not.exist")
  });

  it('Bouton Ajouter un matériel',() => {
    // test de l'ajout de matériel générique
    cy.get(".card-header .btn-group > .btn-group a").contains("Ajouter un matériel").click()
    cy.get(".card-header .btn-group > .btn-group ul").contains("Générique").click()
    cy.url().should("contain","/entity/1/materials/g/new")

    // retour à la page précédente
    cy.visit("/#/entity/1/materials/")

    cy.get(".card-header .btn-group > .btn-group a").contains("Ajouter un matériel").click()
    cy.get(".card-header .btn-group > .btn-group ul").contains("Spécifique").click()
    cy.url().should("contain","/entity/1/materials/s/new")

    // retour à la page précédente
    cy.visit("/#/entity/1/materials/")

    cy.get(".card-header .btn-group > .btn-group a").contains("Ajouter un matériel").click()
    cy.get(".card-header .btn-group > .btn-group ul").contains("Générique massif").click()
    cy.url().should("contain","/entity/1/materials/g/bulk")
  });

  it('Vérification des boutons pour un matériel - Modifier', () => {
    // bouton modifier
    cy.get(".card-body table > tbody > tr").contains("STM32WB555").parent().find("td:last a").contains("Modifier").click()
    cy.url().should("contain","/entity/1/materials/g/2")
    cy.get("#name").should("have.value","STM32WB555")
    cy.get("#refMan").should("have.value","P-NUCLEO-WB55")
    // dans la page de modification test bouton de suppression
    cy.contains("Supprimer").click()
    cy.get(".modal-content").should("exist").and("contain","Voulez vous vraiment supprimer")
    cy.get(".modal-content button").contains("Non").click()
    cy.get(".modal-content").should("not.exist")
    cy.url().should("contain","/entity/1/materials/g/2")
    // annulation de la modification
    cy.get(".card-body .btn-group button").contains("Annuler").click()
    cy.url().should("contain","/entity/1/materials/").and("not.contain","g/2")
  });

  it('Vérification des boutons pour un matériel - Voir les prêts', () => {
    // bouton modifier
    cy.get(".card-body table > tbody > tr").contains("STM32WB555").parent().find("td:last a").contains("Voir les prêts").click()
    cy.url().should("contain","/entity/1/materials/g/2/loans")
    cy.get(".card-header h3").should("contain","STM32WB555")

    // INFO : Pour les tests sur cette page des prêts, des tests sont effectués sur la même page dans /test_mes-prêts ou dans le bloc de tests suivant

    // bouton retour
    cy.get(".card-header a").contains("Retour").click()
    cy.url().should("contain","/entity/1/materials/").and("not.contain","g/2/loans")
  });
});

describe("Gestion entité - Page Gestion des Prêts", () => {
  beforeEach(() => {
    cy.viewport(width,height)

    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get(".dropdown-item").contains("FabMSTIC").click()
    // clic sur le bouton "Gestion Prêts"
    cy.get(".btn").contains("Gestion prêts").click()
  });

  after(() => {
    // suppression du dossier des téléchargements de l'environnement local de Cypress
    let downloadsFolder = Cypress.config('downloadsFolder')
    cy.task('deleteFolder', downloadsFolder)
  })

  it('Bouton Retour', () => {
    // test du bouton de retour
    cy.get(".card-header a").contains("Retour").click()
    cy.url().should("contain","/entity/1").and("not.contain","/loans")
  });

  it("Bouton de téléchargement de l'archive", () => {
    // clic sur le bouton
    cy.get("#DL_arch").click()
    // vérification de l'existence du fichier (le contenu dépend du backend et sera testé dans la back)
    let chaineAnnee = (dDate.getFullYear()-1).toString() // archive toujours année précédente donc -1
    cy.readFile("./cypress/downloads/Données Archivées_Année "+ chaineAnnee +".json").should("exist")
  });

  it("Bouton Modifier d'un prêt", () => {
    // vérification du premier prêt (pour savoir sur quoi on clique)
    cy.get(".card-body table tbody tr:first td:first ul").should("contain","Asus T3")
    // vérification et clique sur le bouton Modifier
    cy.get(".card-body table tbody tr:first > td:last > button").click()
    cy.url().should("contain","/loan/1")
    // page de modification testé pour les matériels
    // annulation de la modification
    cy.get(".card-body .btn-group button").contains("Annuler").click()
    cy.url().should("contain","/entity/1/loans")
  });

  // le reste de la page est testé dans /test_mes-prêts
});

describe("Gestion entité - Page Statistiques", () => {
  beforeEach(() => {
    cy.viewport(width,height)

    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get(".dropdown-item").contains("FabMSTIC").click()
    // clic sur le bouton "Statistiques"
    cy.get(".btn").contains("Statistiques").click()
  });

  it('Bouton Retour', () => {
    // test du bouton de retour
    cy.get(".card-header a").contains("Retour").click()
    cy.url().should("contain","/entity/1").and("not.contain","/stats")
  });

  it('Repliage des blocs latéraux', () => {
    // bloc Choix Type Statistique
    cy.get("form").contains("Choix Type Statistique").parent().parent().find(".card-body").should("exist")
    cy.get("form").contains("Choix Type Statistique").parent().click()
    cy.get("form").contains("Choix Type Statistique").parent().parent().find(".card-body").should("not.exist")
    // bloc Choix du Tri
    cy.get("form").contains("Choix du Tri").parent().parent().find(".card-body").should("exist")
    cy.get("form").contains("Choix du Tri").parent().click()
    cy.get("form").contains("Choix du Tri").parent().parent().find(".card-body").should("not.exist")
    // autres bloc possèdent le même fonctionnement
  });

  it('Apparition bloc latéral - filtre sur fréquence', () => {
    // vérification de la non présence du bloc de filtre sur fréquence
    cy.get("form").contains("Choix du Filtrage sur fréquence").should("not.exist")
    // sélection de la statistique "fréquence d'emprunt"
    cy.get("form").contains("Choix Type Statistique").parent().parent().find(".card-body > div:last input").click()
    // vérification apparition du bloc de filtre sur fréquence
    cy.get("form").contains("Choix du Filtrage sur fréquence").should("exist")
  });

  it('Apparition bloc latéral - filtre sur tri par affiliation', () => {
    // vérification de la non présence du bloc de filtrage par type d'affiliation
    cy.get("form").contains("Choix du Filtrage par type d'affiliation").should("not.exist")
    // sélection de la statistique "fréquence d'emprunt"
    cy.get("form").contains("Choix du Tri").parent().parent().find(".row .card-body:first > div:first input").click()
    // vérification apparition du bloc de filtrage par type d'affiliation
    cy.get("form").contains("Choix du Filtrage par type d'affiliation").should("exist")
  });

  it("Apparition page d'aide", () => {
    // vérification que la page principale est affichée
    cy.get(".corps > div:last .pagination").should("exist")
    cy.get(".corps > div:last .table-responsive").should("exist")
    cy.get(".corps > div:last .card-header h3").should("have.text","FabMSTIC: Statistiques")

    // clic sur le bouton d'aide
    cy.get("form").contains("Choix du Type de traitement de la plage d'analyse").parent().find("button").click()
    // vérification de l'apparition de la page d'aide
    cy.get(".corps > div:last .pagination").should("not.exist")
    cy.get(".corps > div:last .table-responsive").should("not.exist")
    cy.get(".corps > div:last .card-header h3").should("contain","Aide : Type de traitement")

    // validation de la page d'aide (et disparition)
    cy.get(".corps > div:last .card-body button").click()
    // vérification que la page principale est affichée
    cy.get(".corps > div:last .pagination").should("exist")
    cy.get(".corps > div:last .table-responsive").should("exist")
    cy.get(".corps > div:last .card-header h3").should("have.text","FabMSTIC: Statistiques")
  });

  /* it("Calcul d'une statistique", () => {
    // sélection de la statistique "Nombre d'emprunt"
    cy.get("form").contains("Choix Type Statistique").parent().parent().find(".card-body > div:first input").click()
    // sélection du tri par Affiliation
    cy.get("form").contains("Choix du Tri").parent().parent().find(".row .card-body:first > div:first input").click()
    // clic sur le bouton de calcul
    cy.contains("Calculer les Statistiques").should("not.be.disabled")
    cy.contains("Calculer les Statistiques").click()

    // vérification de l'apparition du tableau des résultats
    cy.get(".corps > div:last .card-body thead").should("exist")
      // header du tableau
    cy.get(".corps > div:last .card-body table thead > tr > th:first").should('have.text','Affiliation')
    cy.get(".corps > div:last .card-body table thead > tr > th:last").should('have.text','Nombre d emprunts')
      // corps tableau
    cy.get(".corps > div:last .card-body table tbody > tr").should('have.length',10)
    cy.get(".corps > div:last .card-body table tbody > tr:first > td:first").should('have.text',"Polytech Grenoble")
    cy.get(".corps > div:last .card-body table tbody > tr:first > td:last").should('have.text',"469")
  }); */

  /* it("Bouton Ordre", () => {
    // calcul d'une statistique pour pouvoir changer l'ordre
    cy.get("form").contains("Choix Type Statistique").parent().parent().find(".card-body > div:first input").click()
    cy.get("form").contains("Choix du Tri").parent().parent().find(".row .card-body:first > div:first input").click()
    cy.contains("Calculer les Statistiques").should("not.be.disabled")
    cy.contains("Calculer les Statistiques").click()
  }); */

  /* it("Téléchargement des résultats d'un calcul", () => {
    //
  }); */
});

describe("Gestion entité - Edition", () => {
  beforeEach(() => {
    cy.viewport(width,height)

    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get(".dropdown-item").contains("FabMSTIC").click()
    // clic sur le bouton "Editer" (icône de crayon)
    cy.get(".btn-circle").click()
  });

  it('Champs', () => {
    // vérification de champ du nom
    cy.get("#name").should("have.value","FabMSTIC")
    // vérification du champ de contact
    cy.get("#contact").should("have.value","fabmstic@univ-grenoble-alpes.fr")
    // vérification de la liste des manageurs
    cy.get(".corps .card-body > form > div:first > div:last > div:first > ul > li")
    .should("have.length",4)
    .should("contain","Germain Lemasson")
    .should("contain","Noe Boulaye")
    .should("contain","Anthony Geourjon")
    .should("contain","Admin admin")
    // vérification de la liste des affiliations
    cy.get(".corps .card-body > form > div:first > div:last > div:last > ul > li")
    .should("have.length",2)
    .should("contain","LIG")
    .should("contain","FabMSTIC")
  });

  it('Bouton Aide', () => {
    // vérification du bouton d'aide
    cy.get("#modal-syntaxe").should("not.exist")
    cy.contains("Aide").click()
    cy.get("#modal-syntaxe").should("exist")
    cy.get("#modal-syntaxe .btn").contains("Ok").click()
    cy.get("#modal-syntaxe").should("not.exist")
  });
});