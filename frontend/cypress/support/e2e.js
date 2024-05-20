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
// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

Cypress.on('uncaught:exception', (err, runnable, promise) => {
    return false
})

/*
Uncaught exceptions :
    X.value is null => Quand retour à la page d'emprunt de matériel grâce au bouton "Ajouter un matériel" du panier.

    AxiosError: Request aborted => Quand on effectue une recherche par nom complet, par chiffre ou avec plusieurs lettres collées 
                                   dans la barre de recherche de la page de la liste d'entités.
    AxiosError: Request aborted => Quand on se redirige vers la page de la liste d'entités grâce au bouton de la navbar et/ou au lien de la page d'accueil.
    AxiosError: Request aborted => Quand on se redirige vers la page du panier grâce au bouton du haut de page.
    AxiosError: Request aborted => Quand on se redirige vers la page d'accueil de Matos depuis le lien du footer.
    AxiosError: Request aborted => Quand on se redirige vers les infos d'une entité depuis la page d'emprunt de matériel 
                                   (petit lien, portant le nom de l'entité dans la boîte de chaque matériel).
*/
/*
Errors :
    Page liste des prêts ("Mes prêts"), erreur dans la consultation d'un prêt, 
        la requête API pour obtenir l'utilisateur remplace également l'affiliation du prêt (uniquement pour l'affichage).
*/