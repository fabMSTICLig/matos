const width = 760
const height = 1024

describe("Liste des entités", () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // sélection puis clic sur le bouton de la barre de navigation nommé "Emprunt Matériel"
    cy.get("nav").contains("Emprunt Matériels").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // clic sur le bouton ("Ajouter au panier") du premier matériel de la liste (STM32WB555)
    cy.get(".row > .col > .card > .card-body > ul > li:first > .btn").click()
    // clic sur le bouton Panier
    cy.get("nav .btn").contains("Panier").click()
  });

  it('Element présent dans le panier', () => {
    // test du nombre d'éléments dans la liste des éléments
    // 1 par défaut pour le bouton "Ajouter un Matériel"
    cy.get(".corps table > tbody > tr").should("have.length",2)
    // vérification de l'élément présent
    cy.get(".corps table > tbody > tr:first > td:first").should("contain","STM32WB555")
  });

  it('Bouton X', () => {
    // vérification de la non présence d'un texte de prévention
    cy.get(".corps .text-danger").should("not.be.exist")
    // test du nombre d'éléments dans la liste des éléments
    // 1 par défaut pour le bouton "Ajouter un Matériel"
    cy.get(".corps table > tbody > tr").should("have.length",2)

    // clic sur le bouton X du matériel présent dans le panier
    cy.get(".corps table > tbody > tr:first > td:last > button").click()
    // test du nombre d'éléments dans la liste des éléments
    cy.get(".corps table > tbody > tr").should("have.length",1)
    // vérification de la modification du panier (au niveau du bouton)
    cy.get(".liste-secondaire a").contains("Panier").should("contain","Panier (0)")
    // vérification de l'apparition d'un texte de prévention
    cy.get(".corps .text-danger").should("be.exist")
  });

  it('Bouton Vider le panier', () => {
    // vérification de la non présence d'un texte de prévention
    cy.get(".corps .text-danger").should("not.be.exist")
    // test du nombre d'éléments dans la liste des éléments
    // 1 par défaut pour le bouton "Ajouter un Matériel"
    cy.get(".corps table > tbody > tr").should("have.length",2)
    
    // clic sur le bouton Vider Panier
    cy.contains("Vider panier").click()
    // test du nombre d'éléments dans la liste des éléments
    cy.get(".corps table > tbody > tr").should("have.length",1)
    // vérification de la modification du panier (au niveau du bouton)
    cy.get(".liste-secondaire a").contains("Panier").should("contain","Panier (0)")
    // vérification de l'apparition d'un texte de prévention
    cy.get(".corps .text-danger").should("be.exist")
  });

  it('Bouton Ajouter un matériel', () => {
    // clic sur le bouton "Ajouter un matériel" de la page panier
    cy.contains("Ajouter un matériel").click()
    // vérification du changement de page
    cy.url().should("contain","/search")
  });
});