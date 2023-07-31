const width = 1620
const height = 1080
const dDate = new Date()

describe("Liste des entités", () => {
  after(() => {
    // suppression du dossier des téléchargements de l'environnement local de Cypress
    let downloadsFolder = Cypress.config('downloadsFolder')
    cy.task('deleteFolder', downloadsFolder)
  })

  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de profil
    cy.get(".btn").contains("admin").click()
    // sélection puis clic sur le bouton "Profile" du menu déroulant
    cy.get(".dropdown-item").contains("Profile").click()
  });

  it('Valider', () => {
    // clic sur le bouton Valider
    cy.contains("Valider").click()

    // vérification d'apparition du bloc d'avertissement
    cy.get(".modal").should("be.exist")
    // vérification texte du bloc d'avertissement
    cy.get(".modal-body > p").should("contain","Profile mis à jour")
    // clic sur le bouton Ok du bloc d'avertissement
    cy.contains("Ok").click()
    // vérification disparition du bloc d'avertissement
    cy.get(".modal").should("not.be.exist")
  });

  it('Télécharger mes données', () => {
    // clic sur le bouton de téléchargement de ses données personnelles
    cy.contains("Télécharger mes données").click()
    // Vérifie le téléchargement d'un fichier
    let chaineJour = dDate.getDate().toString() + (dDate.getMonth()+1).toString() + dDate.getFullYear().toString()
    cy.readFile("./cypress/downloads/admin_"+ chaineJour +".json").should("exist")
  })

  it('Champs', () => {
    // test du champ Username
    cy.get("input#username").should("have.value","admin")
    // test du champ Prénom
    cy.get("input#firstname").should("have.value","Admin")
    // test du champ Nom
    cy.get("input#lastname").should("have.value","admin")
    // test du champ Email
    cy.get("input#email").should("have.value","aa@aa.aa")
    // test du champ Affiliations
    cy.get("ul.list-group > li:first > span").should("have.text","FabMSTIC")
  })
});