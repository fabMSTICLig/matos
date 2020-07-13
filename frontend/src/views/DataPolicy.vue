<template>
  <div class="row justify-content-center">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
         <h4>Traitement des données</h4>
        </div>
        <div class="card-body scroll">
          <section>
            <article>
              <h3>Destinataires</h3>
                <p align="justify"> Chaque entité, composante universitaire, école, laboratoire ou plateforme pédagogique representée par un ayant droit,
                  dispose de ses données sur la plateforme.
              </p>
            </article>
            <article>
              <h3>Stockage des informations</h3>
                <p align="justify">
                  Pour permettre le bon fonctionnment du site, certaines de vos
                  informations sont stockées au moyen d'un cookie. Votre login <b><i>Agalan</i></b> vous permet d'utiliser la plateforme, et le nom d'utilisateur est enregistré pendant la session.
                </p>
                <h4>Objet</h4>
                <p align="justify">
                  <b>Nom d'utilisateur</b>, <b>Prénom</b>, <b>Nom</b>, <b>Email</b> sont utilisés afin de vous
                  contacter. Seul les <b><i>managers</i></b> des entités ont accés à ces informations.
                </p>
                <p align="justify">
                  Un historique des prêts de matériels est mis en place, permettant à chaque entité de disposer des ses informations.
                </p>
            </article>
            <article>
              <h3>Durée de stockage</h3>
              <p align="justify">
              Ces informations ainsi que celles liées aux prêts de matériels, seront stockées autant de temps que
              vous êtes actif au sein de l'université, écoles ou établissements de recherche. Elles seront également conservées au delà de la durée de votre départ.
              </p>
            </article>
            <article>
              <h3>Accès aux données personnelles</h3>
              <p align="justify">A tout moment, vous pouvez demander un accès aux données vous concernant, rectifier ou supprimer vos données avec le formulaire suivant : </p>
              <p align="justify">Ou sur demande avec vos interlocuteurs:</p>
                <ul>
                  <li>relaisdpo@grenoble-inp.fr</li>
                  <li>dpo@grenet.fr</li>
                </ul>
            </article>
            <article>
              <h3>Sécurité des données</h3>
              <ol>
                <li>Les données enregistrées concernant les entités et les prêts sont accessibles uniquement aux utilisateurs ayant les droits d'accès de celles-ci,
                et non visible pour les autres utilisateurs sans permissions.</li>
                 <li align="justify">Les données sont archivées régulièrement et permettent de retrouver l'historique des informations et des prêts de matériels pour toute entité.
                </li>
              </ol>
            </article>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// @ is an alias to /src

export default {
  name: "DataPolicy",
  components: {}
};
</script>
<style scoped>
  .row {
    margin-top: 60px;
  }
  ol {
  list-style-type: none;
  /*use padding to move list item from left to right*/
  padding-left: 1em;
  }

  ol li {
    text-align: justify;
  }

  ol li:before {
  content: "-";
  position: absolute;
  /*change margin to move dash around*/
  margin-left: -1em;
  }
  .scroll {
    max-height: 450px;
    overflow-y: scroll;
  }
</style>
