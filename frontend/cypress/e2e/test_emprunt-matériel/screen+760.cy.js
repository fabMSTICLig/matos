/*
 * Copyright (C) 2020-2024 LIG Université Grenoble Alpes
 *
 *
 * This file is part of Matos.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * Matos is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
 * @author Clément Lesaulnier
 * @author Robin Courault
*/
const width = 760
const height = 1024

describe("Pagination", () => {
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
    cy.contains("Emprunt Matériels").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
  });

  it('Chargement correct', () => {
    // vérification qu'au chargement de la page d'emprunt du matériel, page 1 sélectionnée
    cy.get(".pagination .page-link").contains("1").parent().should("have.class","active")
  })

  it('Bouton numéro de page', () => {
    // clic sur le bouton 2 (+1)
    cy.get(".pagination .page-link").contains("2").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("2").parent().should("have.class","active")

    // clic sur le bouton 1 (-1)
    cy.get(".pagination .page-link").contains("1").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("1").parent().should("have.class","active")

    // clic sur le bouton 3 (+2)
    cy.get(".pagination .page-link").contains("3").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("3").parent().should("have.class","active")

    // bouton numéro 1 (-2)
    // clic sur le bouton 1 qui ne doit plus exister
    cy.get(".pagination .page-link").contains("1").should("not.exist")
    // vérification de l'existence d'un bouton 4
    cy.get(".pagination .page-link").contains("4").should("exist")
    // clic sur le bouton 2 puis le bouton 1 pour effectuer le retour à 2 pages avant
    cy.get(".pagination .page-link").contains("2").click()
    cy.get(".pagination .page-link").contains("1").click()

    // bouton numéro 4 (+3) ne doit pas exister (depuis la page 1)
    cy.get(".pagination .page-link").contains("4").should("not.exist")

    // bouton numéro 0 (-1) ne doit pas exister (depuis la page 1)
    cy.get(".pagination .page-link").contains("0").should("not.exist")
  });

  it('Bouton suivant', () => {
    // clic sur le bouton suivant
    cy.get(".pagination .page-link").contains("Suivant").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("2").parent().should("have.class","active")
  });

  it('Bouton précédent', () => {
    // passage à la page 2, pour utilisation du bouton
    cy.get(".pagination .page-link").contains("2").click()

    // clic sur le bouton suivant
    cy.get(".pagination .page-link").contains("Précédent").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("1").parent().should("have.class","active")
  });

  it('Bouton dernier', () => {
    // clic sur le bouton suivant
    cy.get(".pagination .page-link").contains("Dernier").click()
    // vérification du changement de page
    cy.get(".pagination .page-link").contains("Suivant").parent().should("have.class","disabled")
    cy.get(".pagination .page-link").contains("Dernier").parent().should("have.class","disabled")
    cy.get("ul.pagination>li").eq(4).should("have.class","active")
  });

  it('Bouton premier', () => {
    // clic sur le bouton suivant 3 fois
    for (let index = 0; index < 3; index++) {
      cy.get(".pagination .page-link").contains("Suivant").click()
    }
    // vérification que le bouton 1 n'existe pas (=> et qu'il n'est donc pas actif)
    cy.get(".pagination .page-link").contains("1").should("not.exist")

    // clic sur le bouton premier
    cy.get(".pagination .page-link").contains("Premier").click()

    // vérification du changement de page
    cy.get(".pagination .page-link").contains("Précédent").parent().should("have.class","disabled")
    cy.get(".pagination .page-link").contains("Premier").parent().should("have.class","disabled")
    cy.get("ul.pagination>li").eq(2).should("have.class","active")
  });

  it('Désactivation correcte des boutons précédent et premier', () => {
    // on arrive sur la page 1 (vérification effectué plus haut)
    // => les boutons précédent et premier doivent être désactivés
    cy.get(".pagination .page-link").contains("Précédent").parent().should("have.class","disabled")
    cy.get(".pagination .page-link").contains("Premier").parent().should("have.class","disabled")
  });

  it('Désactivation correcte des boutons suivant et dernier', () => {
    // on se déplace sur la dernière page, testé précédemment
    cy.get(".pagination .page-link").contains("Dernier").click()
    // => les boutons suivant et dernier doivent être désactivés
    cy.get(".pagination .page-link").contains("Suivant").parent().should("have.class","disabled")
    cy.get(".pagination .page-link").contains("Dernier").parent().should("have.class","disabled")
  });
});

/*
// TODO : tests sur les filtres
describe("Filters", () => {
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
    cy.contains("Emprunt Matériels").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
  });

  it('La recherche', () => {

//  WARN : le champ de recherche regarde tous les champs d'un matériel,
//        même ceux non visibles depuis la page d'emprunt
  });

  it('Le type', () => {

  });

  it('Filtres par entité', () => {

  });

  it('Filtres par tag', () => {

  });
});
*/

describe("Materials List", () => {
  // WARN : Dysfonctionnement des tests si le premier matériel de la liste n'appartient pas au FabMSTIC

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
    cy.contains("Emprunt Matériels").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
  });

  it('Ajout au panier', () => {
    // initialement le panier est à 0
    cy.get(".liste-secondaire a").contains("Panier").should("contain","Panier (0)")

    // association à l'alias "select" du bouton ("Ajouter au panier") du premier matériel de la liste
    cy.get(".row > .col > .card > .card-body > ul > li:first > .btn").as("select")
    // clic sur le bouton
    cy.get('@select').click()
    // vérification de la modification du panier
    cy.get(".liste-secondaire a").contains("Panier").should("contain","Panier (1)")

    // vérification de l'ajout du filtre d'entité
    cy.get("form .multiselect-tags:first").should("have.length.gt", 0)
    // vérification du filtre
    cy.get("form .multiselect-tags:first .multiselect-tag").should("contain",'FabMSTIC')

    // vérification de la désactivation du bouton et de son changement de message
    cy.get('@select').should("contain","Déjà dans le panier").and("be.disabled")
  });

  it('Infos sur matériel', () => {
    // WARN : Dysfonctionnement du test si le premier matériel ne correspond pas au STM32WB555 par défaut
    // TODO : Ajouter le test de texte identique + ajouter le test des tags identiques
    
    // clic sur le lien titre du matériel
    cy.get(".row > .col > .card > .card-body > ul > li:first > div:first > a").click()
    // vérification du changement de page
    cy.url().should("contain","/materials/g")
    cy.get(".card h3").should("have.text","STM32WB555")
  });

  it('Infos sur entité', () => {
    // clic sur le lien entité du matériel
    cy.get(".row > .col > .card > .card-body > ul > li:first > div:first > strong > a").click()
    // vérification du changement de page
    cy.url().should("contain","/entity")
    cy.get(".card h3").should("have.text","FabMSTIC")
  });
});