<template>
  <div class="row justify-content-center">
    <div class="col-12 col-md-12">
      <div class="card">
        <div class="card-header">
          <h4>Traitement des données</h4>
        </div>
        <div class="card-body scroll">
          <section>
            <article>
              <h3>Destinataires</h3>
              <p align="justify">
                Chaque entité, composante universitaire, école, laboratoire ou
                plateforme pédagogique representée par un ayant droit, dispose
                de ses données sur la plateforme.
              </p>
            </article>
            <article>
              <h3>Stockage des informations</h3>
              <p>
                Pour permettre le bon fonctionnment du site certaines de vos
                informations sont stockées au moyen d'un cookie. Votre login
                <i>Agalan</i> vous permet d'utiliser la plateforme, et le nom
                d'utilisateur est enregistré pendant la session. Un cookie est
                également utilisé pour enregistrer le prêt en cours
                d'utilisation (création ou modification)
              </p>
              <h4>Données utilisées</h4>
              <p>
                Nom d'utilisateur, Prénom, Nom, Email sont utilisés afin de vous
                contacter. Les managers des entités et les administrateur du
                site ont accés à ces informations.
              </p>
            </article>
            <article>
              <h3>Durée de stockage</h3>
              <p>
                Ces informations ainsi que celles liées aux prêts seront
                stockées 1 ans après que vous ayez quitté l'université ou sur
                demande aux adresses :
              </p>
              <ul>
                <li>relaisdpo@grenoble-inp.fr</li>
                <li>dpo@grenet.fr</li>
              </ul>
            </article>
            <article>
              <h3>Accès aux données personnelles</h3>
              <p>
                A tout moment, vous pouvez demander un accès aux données vous
                concernant, rectifier ou supprimer vos données avec les contacts
                cités précédemment
              </p>
            </article>
            <article>
              <h3>Sécurité des données</h3>
              Les données enregistrées concernant les entités et les prêts sont
              accessibles aux managers des entités concernées et aux
              administrateurs du site.
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
