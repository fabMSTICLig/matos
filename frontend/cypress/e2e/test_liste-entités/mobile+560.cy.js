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
const width = 560
const height = 760

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
    // sélection puis clic sur le bouton de la barre de navigation nommé "Liste Entités"
    cy.contains("Liste Entités").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()

    // préselection des deux blocs composant la page
    cy.get(".corps > div:last").as("rightBloc")
  });

  it('Ligne de tableau - clic sur un élément', () => {
    // sélection de la ligne contenant le nom "TIMA"
    cy.get(".corps > div:first").contains("TIMA").as("select")

    // vérification que la ligne n'est pas active
    cy.get("@select").parent().should("not.have.class","table-active")
    // vérification que le bloc de droite n'affiche pas les informations sur l'entité TIMA
    cy.get("@rightBloc").should("not.contain","TIMA")

    // clic sur la ligne TIMA
    cy.get("@select").click()
    // vérification que la ligne est active
    cy.get("@select").parent().should("have.class","table-active")
    // vérification que le bloc de droite affiche les informations sur l'entité TIMA
    cy.get("@rightBloc").should("contain","TIMA")
  });

  it('Recherche - nom complet', () => {
    // sélection de la barre de recherche et remplissage par "TIMA"
    cy.wait(300).get("input[type=search]").type("TIMA")

    // vérification que le tableau ne contient plus que 1 élément
    cy.wait(200).get("table.table > tbody").should("have.length",1)
    // vérification que cet élément est celui recherché
    cy.get("table.table > tbody > tr > td").should("have.text","TIMA")
    // vérification que cet élément est actif (sans besoin de clic)
    cy.get("table.table > tbody > tr").should("have.class","table-active")
    // vérification que le bloc de droite affiche les informations sur l'entité TIMA
    cy.get("@rightBloc").should("contain","TIMA")
  });

  it('Recherche - lettre unique', () => {
    // sélection de la barre de recherche et remplissage par "a"
    //  => non prise en compte de la casse souhaitée
    cy.get("input[type=search]").type("a")

    // vérification que le tableau ne contient plus que 4 éléments
    cy.wait(200).get("table.table > tbody > tr").should("have.length",4)
  });

  it('Recherche - lettre multiples collées', () => {
    // sélection de la barre de recherche et remplissage par "ms"
    //  => non prise en compte de la casse souhaitée
    cy.wait(300).get("input[type=search]").type("ms")

    // vérification que le tableau ne contient plus que 2 éléments
    cy.wait(200).get("table.table > tbody > tr").should("have.length",2)
  });

  it('Recherche - lettre multiples espacées', () => {
    // sélection de la barre de recherche et remplissage par "ms"
    //  => non prise en compte de la casse souhaitée
    //  => chaque lettre doit être présente mais peut importe l'ordre ou si elles sont collées
    cy.wait(300).get("input[type=search]").type("m a")

    // vérification que le tableau ne contient plus que 3 éléments
    cy.wait(200).get("table.table > tbody > tr").should("have.length",3)
  });

  it('Recherche - chiffre', () => {
    // sélection de la barre de recherche et remplissage par "1"
    //  => aucun nom d'entité avec un chiffre
    cy.get("input[type=search]").type("1")

    // vérification que le tableau ne contient plus que 0 éléments
    cy.wait(200).get("table.table > tbody > tr").should("have.length",0)
  });
});

describe("Description entité", () => {
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
    // sélection puis clic sur le bouton de la barre de navigation nommé "Liste Entités"
    cy.contains("Liste Entités").click()
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
  });

  it('Bouton voir matériel', () => {
    //
    cy.get(".table-active td").should("have.text","FabMSTIC")
    // 
    cy.contains("Voir le matériels").click()
    //
    cy.url().should("contain","/search")
    cy.get(".multiselect:first > .multiselect-wrapper > .multiselect-tags > span").should("contain","FabMSTIC")
  });
});