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
const width = 1620
const height = 1080

describe('tests des pages admin - Utilisateurs', () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant Admin
    cy.get("a").contains("Admin").click()
    // sélection puis clic sur le bouton "Utilisateurs" du menu déroulant
    cy.get(".dropdown-item").contains("Utilisateurs").click()
  })

  it('Recherche', () => {
    // Une unique lettre => ne doit pas afficher d'utilisateurs, 3 caractères minimum requis
    cy.get("#searchInput").type("g")
    cy.get(".corps .card-body table tbody").should("be.empty")
    // 4 lettres ('germ') => doit afficher 2 utilisateurs
    cy.get("#searchInput").type("{backspace}germ")
    cy.get(".corps .card-body table tbody").should("not.be.empty")
    cy.get(".corps .card-body table tbody > tr").should("have.length",2)
  });

  it('Bouton Modifier', () => {
    // clic sur le bouton modifier de la première ligne, élément utilisateur "Germain Lemasson"
    cy.get(".corps .card-body table tbody > tr:first > td:last").contains("Modifier").click()
    // vérification de l'url pour l'utilisateur "Germain Lemasson"
    cy.url().should("contain","/users/1")
  });
})

describe('tests des pages admin - Tags', () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')
    
    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant Admin
    cy.get("a").contains("Admin").click()
    // sélection puis clic sur le bouton "Tags" du menu déroulant
    cy.get(".dropdown-item").contains("Tags").click()
  })

  it('Recherche', () => {
    // 2 lettres ('el') => doit afficher 3 tags
    cy.get("#searchInput").type("el")
    cy.get(".corps .card-body table tbody").should("not.be.empty")
    cy.get(".corps .card-body table tbody > tr").should("have.length",3)
  });

  it('Bouton Modifier', () => {
    // clic sur le bouton modifier de la première ligne, élément tag "info"
    cy.get(".corps .card-body table tbody > tr:first > td:last").contains("Modifier").click()
    // vérification de l'url pour le tag "info"
    cy.url().should("contain","/tags/3")
  });
})

describe('tests des pages admin - Affiliations', () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')
    
    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant Admin
    cy.get("a").contains("Admin").click()
    // sélection puis clic sur le bouton "Affiliations" du menu déroulant
    cy.get(".dropdown-item").contains("Affiliations").click()
  })

  it('Recherche', () => {
    // 2 lettres ('Fa') => doit afficher 1 affiliation
    cy.get("#searchInput").type("Fa")
    cy.get(".corps .card-body table tbody").should("not.be.empty")
    cy.get(".corps .card-body table tbody > tr").should("have.length",1)
  });

  it('Bouton Modifier', () => {
    // clic sur le bouton modifier de la première ligne, élément affiliation "LIG"
    cy.get(".corps .card-body table tbody > tr:first > td:last").contains("Modifier").click()
    // vérification de l'url pour l'affiliation "LIG"
    cy.url().should("contain","/affiliations/1")
  });
})