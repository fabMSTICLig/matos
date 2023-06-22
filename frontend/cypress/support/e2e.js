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