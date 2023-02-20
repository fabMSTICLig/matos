<template>
  <div class="row justify-content-center">
    <div class="col-12 col-md-12">
      <div class="card">
        <div class="card-header">
          <h4>Le site MATOS</h4>
        </div>
        <div class="card-body">
          <h4>Contexte</h4>
          <p class="text-justify">
            Pour réduire son impact écologique, la première étape est de moins
            et mieux consommer.
          </p>

          <p class="text-justify">
            L'université possède beaucoup de matériels à des fins pédagogiques
            et de recherche. Ces matériels sont répartis dans les nombreuses
            composantes universitaires, écoles d'ingénieurs, laboratoires de
            recherche et services qui lui sont rattachés. Parfois certains
            matériels sont inutilisés pendant de longues périodes et les
            différentes entités, qui les possèdent, sont disposé à prêter ces
            matériels. Cependant, il est difficile de savoir qui possède quoi et
            ce qui est disponible.
          </p>

          <p class="text-justify">
            Pour cette raison, le site de prêt Matos a été créé afin d'aider à
            la mutualisation du matériel. L'idée est que toutes entités de
            l'université puissent mettre à disposition le matériel qu'elle
            souhaite.
          </p>
          <h6>
            <router-link :to="{ name: 'search' }"
              >Emprunter du matériel >>
            </router-link>
          </h6>
          <p>
            Pour emprunter du matériel, ajoutez le(s) matériel(s) souhaité(s) à
            votre panier, indiquez la date d'emprumt souhaitée. Une demande de
            prêt sera automatiquement envoyée à l'entité concerné. Elle vous
            répondra dans les meilleurs délais.
          </p>
          <h6>
            <router-link :to="{ name: 'showentities' }"
              >Voir les entités mettant à disposition du matériel >>
            </router-link>
          </h6>
          <p>
            Vous pouvez consultez toutes les entités proposant du matériel à
            l'emprunt. Remarque: une entité peut être un laboratoire, un service
            dans un laboratoire, une composante universitaire, une plateforme
            technique, un fablab, ...
          </p>
          <h6>
            <a :href="'mailto:matos'+'@'+'univ-grenoble-alpes.fr'"
              >Prêtez du matériel >>
            </a>
          </h6>
          <p>
            Si vous souhaitez prêter du matériel, contacter un administrateur du
            site afin qu'il crée une entité. Vous pourrez alors définir le(s)
            manageur(s) de votre entité, ajouter du matériel proposé à l'emprumt
            et gérer les prêts depuis le site.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppHome",
};
</script>

<script setup></script>
