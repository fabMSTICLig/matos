const width = 560
const height = 760

describe("Mes prêts", () => {
  beforeEach(() => {
    cy.viewport(width,height)
    // procédure identique aux tests d'authentification sans les tests
    cy.visit('/auth/login')

    cy.get("input[name=username]").type("admin")
    cy.get("input[name=password]").type("admin")
    cy.get(".btn").contains("Login").click()

    cy.get(".btn").contains("J'ai compris").click()

    // sélection puis clic sur le menu déroulant de profil
    cy.get("nav .btn").contains("admin").click()
    // sélection puis clic sur le bouton "Mes prêts" du menu déroulant
    cy.get("nav .dropdown-item").contains("Mes prêts").click()
  });

  it('Barre de recherche', () => {
    // recherche d'une entité/affiliation
    cy.get("input[type=search]").type("LIG")
    // vérification de l'affichage des lignes correspondantes
    cy.get("table > tbody > tr").should("have.length",3)

    // recherche d'un matériel "Caméra", => non fonctionnel, souhaité
    cy.get("input[type=search]").type("LIG")
    // vérification
    cy.get("table > tbody").should("not.exist")
  });

  it('Status Selector', () => {
    // comptage du nombre d'options (pour être sûr de la sélection)
    cy.get("select:first > option").should("have.length",5)
    // vérification de l'affichage des lignes correspondantes => par défaut "Tous" donc 3
    cy.get("table > tbody > tr").should("have.length",3)

    // sélection de l'option "Refusé"
    cy.get("select:first").select("Refusé").invoke("val").should("eq","4").wait(500)
    //
    cy.get("table > tbody > tr").should("not.exist")
  });

  it('Order Selector', () => {
    // comptage du nombre d'options (pour être sûr de la sélection)
    cy.get("select:last > option").should("have.length",3)
    // vérification de l'affichage des lignes correspondantes => par défaut "par date de retour prévue" donc prêt avec STM32 est en dernier
    cy.get("table > tbody > tr:last > td > ul > li").should("contain","STM32WB555")

    // sélection de l'option "Date sortie"
    cy.get("select:last").select("Date sortie").wait(500)
    // vérification de l'affichage des lignes correspondantes => prêt avec STM32 est en premier
    cy.get("table > tbody > tr:first > td > ul > li").should("contain","STM32WB555")
  });

  it('Non rendus button', () => {
    // WARN : Peut planter quand le test s'effectue plus vite que les appels Axios
    // => amélioration possible en interceptant les appels et en envoyant via Cypress les données

    // clic sur la case à cocher "non rendus"
    cy.get("#inProgressInput").click()
    // vérification de l'actualisation de la liste de prêts
    cy.get("table > tbody > tr").should("have.length",2)

    // nouveau clic sur la case à cocher
    cy.get("#inProgressInput").click()
    // vérification de l'actualisation de la liste de prêts
    cy.get("table > tbody > tr").should("have.length",3)
  });

  it('Consultation prêt', () => {
    // clic sur bouton "Consulter" du premier prêt affiché (contenant un Melexis MLX90640, une Caméra Wi-Fi M5Stack Unit Cam et une M5Stack ESP32 PSRAM Timer Camera X)
    cy.get("table > tbody > tr:first button").click()
    // vérification de la redirection
    cy.url().should("contain","/loan/256")
    cy.get("#user").parent().find(".multiselect-single-label-text").should("have.text","@admin Admin admin")
    cy.get("#affiliation").parent().find(".multiselect-single-label-text").should("have.text","LIG")
    cy.get("#entity").should("have.value","FabMSTIC")
  });
});