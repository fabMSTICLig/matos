<template>
  <div class="home">
  <div class="row justify-content-center">
    <div class="col-12 col-md-12">
      <div class="card">
        <div class="card-header">
         <h4>La plateforme MATOS</h4>
        </div>
        <div class="card-body">
          <p>La plateforme MATOS a pour but d'aider les différentes entitées de l'université à se prêter du matériel. Par exemple le fablab FabMSTIC prête des cartes arduino dans le cadre de projet pédagogique aux étudiants ENSIMAG et PolyTech Grenoble</p>
          <h4>Quelques définitions utiles pour l'utilisation du site </h4>
          <ul>
            <li>Une <strong>Entité</strong> peut être un laboratoire, une composante universitaire, un service d'un laboratoire, une plateforme technique, ... Chaque entité peut avoir une granularité différente et un fonctionnement différent. Il est donc conseillé de lire la description de l'entité chez qui l'on souhaite emprunter du matériel. Si vous souhaitez prêter du matériel et créer une entité, veuillez contacter les administrateurs du site.</li>
            <li> Il existe deux types de matériel. <strong>Spécifique</strong> et <strong>Générique</strong>
              <ul>
                <li>Le matériel <strong>Spécifique</strong> correspond au matériel dont on ne peut pas intervertir les instances. Par exemple le fablab possède 10 tablettes MarqueX (10 instances), chaque tablette a un numéro de série, s'il prête la tablette 1 (l'instance 1), il est important que ce soit la tablette 1 qui revienne.</li>
                <li>Le matériel <strong>Générique</strong> correpond au matériel dont on peut intervertir les instances. Par exemple le fablab possède des cartes Arduino Uno, quand il prête une carte Arduino Uno, il souhaite qu'une carte Ardduino Uno soit retournée, mais ce n'est pas très grave si ce n'est pas la même que celle prêtée.</li>
              </ul>

            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
    <data-policy></data-policy>
  </div>
</template>

<script>
// @ is an alias to /src
import DataPolicy from "@/views/DataPolicy.vue"

export default {
  name: "Home",
  components: {
    DataPolicy
  }
};
</script>
