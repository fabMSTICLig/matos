<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

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
            différentes entités, qui les possèdent, sont disposées à prêter ces
            matériels. Cependant, il est difficile de savoir qui possède quoi et
            ce qui est disponible.
          </p>

          <p class="text-justify">
            Pour cette raison, le site de prêt Matos a été créé afin d'aider à
            la mutualisation du matériel. <strong>L'idée est que toute entité de
              l'université puisse mettre à disposition le matériel qu'elle
              souhaite.</strong>
          </p>
          <h6>
            <router-link :to="{ name: 'search' }"
              >Emprunter du matériel >>
            </router-link>
          </h6>
          <p>
            Pour emprunter du matériel, ajoutez le(s) matériel(s) souhaité(s) à
            votre panier, indiquez la date d'emprunt souhaitée. Une demande de
            prêt sera automatiquement envoyée à l'entité concernée. Elle vous
            répondra dans les meilleurs délais.
          </p>
          <h6>
            <router-link :to="{ name: 'showentities' }"
              >Voir les entités mettant à disposition du matériel >>
            </router-link>
          </h6>
          <p>
            Vous pouvez consulter toutes les entités proposant du matériel à
            l'emprunt. Remarque : une entité peut être un laboratoire, un service
            dans un laboratoire, une composante universitaire, une plateforme
            technique, un fablab, ...
          </p>
          <h6>
            <a :href="'mailto:matos'+'@'+'univ-grenoble-alpes.fr'"
              >Prêter du matériel >>
            </a>
          </h6>
          <p>
            Si vous souhaitez prêter du matériel, contacter un administrateur du
            site afin qu'il crée une entité. Vous pourrez alors définir le(s)
            manageur(s) de votre entité, ajouter du matériel proposé à l'emprunt
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
