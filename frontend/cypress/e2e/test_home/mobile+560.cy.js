const width = 560
const height = 760

describe('authentification', () => {
  beforeEach(() => {
    cy.viewport(width,height)
  })

  it('successfully admin authentification', () => {
    // connexion à la page http://localhost:8000/auth/login
    cy.visit('/auth/login')
    // vérification que la bonne page est affichée
    cy.url().should('contain','/auth/login')

    // remplissage des champs de connexion
    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    // clic sur le bouton de login
    cy.get(".btn").contains("Login").click()

    // vérification que la connexion s'est bien effectuée grâce au retour sur la page d'accueil
    cy.url().should('contain','/#/')
    // on vérifie également l'absence du bouton login
    cy.get(".btn").contains("Login").should('not.exist')
  });

  it('successfully disconnection (for admin)',  () => {
    // connexion à la page http://localhost:8000/auth/login
    cy.visit('/auth/login')
    // vérification que la bonne page est affichée
    cy.url().should('contain','/auth/login')

    // remplissage des champs de connexion
    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    // clic sur le bouton de login
    cy.get(".btn").contains("Login").click()

    // vérification que la connexion s'est bien effectuée grâce au retour sur la page d'accueil
    cy.url().should('contain','/#/')
    // suppression du panneau des cookies
    cy.get(".btn").contains("J'ai compris").click()
    // clic sur le bouton logout
    cy.get('nav .btn').contains("Logout").click()
    // vérification que la page affichée est bien la page de logout
    cy.url().should('contain','/logout')
  });
})

describe("header's links", () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()
  });

  it('navbar link - Emprunt Matériels', () => {
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // sélection puis clic sur le bouton de la barre de navigation nommé "Emprunt Matériel"
    cy.get("nav").contains("Emprunt Matériels").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/search')
  });

  it('navbar link - Liste Entités', () => {
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // sélection puis clic sur le bouton de la barre de navigation nommé "Liste Entités"
    cy.contains("Liste Entités").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/showentities')
  });

  it('navbar manageur link - Gestion entités - compte admin', () => {
    // Entité FabMSTIC
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("nav a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get("nav .dropdown-item").contains("FabMSTIC").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/entity")
    // vérification du nom de la page
    cy.get(".card-header h3").should('have.text',"FabMSTIC")

    // Entité Domus
    // sélection puis clic sur le menu déroulant de Gestion des entités
    cy.get("nav a").contains("Gestion entités").click()
    // sélection puis clic sur le bouton "FabMSTIC" du menu déroulant
    cy.get("nav .dropdown-item").contains("Domus").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/entity")
    // vérification du nom de la page
    cy.get(".card-header h3").should('have.text',"Domus")
  })

  it('navbar admin link - Admin', () => {
    // Btn Utilisateurs
    // sélection puis clic sur le bouton menu
    cy.get("button.navbar-toggler").click()
    // sélection puis clic sur le menu déroulant Admin
    cy.get("nav a").contains("Admin").click()
    // sélection puis clic sur le bouton "Utilisateurs" du menu déroulant
    cy.get("nav .dropdown-item").contains("Utilisateurs").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/users")

    // Btn Tags
    // sélection puis clic sur le menu déroulant Admin
    cy.get("nav a").contains("Admin").click()
    // sélection puis clic sur le bouton "Tags" du menu déroulant
    cy.get("nav .dropdown-item").contains("Tags").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/tags")

    // Btn Affiliations
    // sélection puis clic sur le menu déroulant Admin
    cy.get("nav a").contains("Admin").click()
    // sélection puis clic sur le bouton "Affiliations" du menu déroulant
    cy.get("nav .dropdown-item").contains("Affiliations").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/affiliations")
  })

  it('header link - Panier', () => {
    // sélection puis clic sur le bouton de panier
    cy.get("nav .btn").contains("Panier").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/basket')
  });

  it('header profil link - Profile', () => {
    // sélection puis clic sur le menu déroulant de profil
    cy.get("nav .btn").contains("admin").click()
    // sélection puis clic sur le bouton "Profile" du menu déroulant
    cy.get("nav .dropdown-item").contains("Profile").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/profile")
  });

  it('header profil link - Mes prêts', () => {
    // sélection puis clic sur le menu déroulant de profil
    cy.get("nav .btn").contains("admin").click()
    // sélection puis clic sur le bouton "Mes prêts" du menu déroulant
    cy.get("nav .dropdown-item").contains("Mes prêts").click()
    // vérification de l'affichage de la bonne page
    cy.url().should("contain","/loans")
  });
})

describe("footer's links", () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()
  });

  it('link - Matos', () => {
    // sélection puis clic sur le bouton "Matos" du footer
    cy.get("a").contains("Matos").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/#/')
  });

  it('link - Mentions légales', () => {
    // sélection puis clic sur le bouton "Mentions légales" du footer
    cy.contains("Mentions légales").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/legalnotice')
  });

  it('link - Traitement des données', () => {
    // sélection puis clic sur le bouton "Traitement des données" du footer
    cy.contains("Traitement des données").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/datapolicy')
  });
})

describe("home's links", () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()
  });

  it('link - Emprunt Matériels', () => {
    // sélection et clic d'un lien nommé "Emprunter du matériel >>"
    cy.get("a").contains("Emprunter du matériel >>").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/search')
  });

  it('link - Liste Entités', () => {
    // sélection et clic d'un lien nommé "Voir les entités mettant à disposition du matériel >>"
    cy.get("a").contains("Voir les entités mettant à disposition du matériel >>").click()
    // vérification de l'affichage de la bonne page
    cy.url().should('contain','/showentities')
  });
})