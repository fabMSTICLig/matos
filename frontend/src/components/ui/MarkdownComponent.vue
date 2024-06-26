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
  <div>
    <div id="editor">
      <div id="markdown" v-html="compiledMarkdown" />
    </div>
    <modal
      id="modal-syntaxe"
      title="Markdown Syntaxe"
      hide-footer
      :show="showHelp"
      :resolve="hideHelp"
    >
      <h6>
        Utilisation de la syntaxe markdown pour modifier la description de
        l'entité :
      </h6>
      <h6>titre de niveau 1 à 6</h6>
      <p># Titre 1</p>
      <p>## Titre 2</p>
      <p>### Titre 3</p>
      <p>###### Titre 6</p>

      <h6>Paragraphes</h6>
      <p>Revenir à la ligne pour les paragraphes</p>
      <h6>Liens</h6>
      <p>[lien entité](https://lien-entité)</p>
      <p>lien avec référence</p>
      <span>[Utilisation d'un numero pour la référence d'un lien][1]</span>
      <p />
      <h6>Listes</h6>
      <i>Numerotée</i>
      <p>1. Element 2. Element</p>
      <i>à Puces</i>
      <p>* Element</p>
      <h6>Séparation</h6>
      <span>---</span>
      <h6>Citations</h6>
      <span> > Citations </span>
      <div class="row justify-content-md-center">
        <button type="button" class="btn btn-primary" @click="hideHelp">
          Ok
        </button>
      </div>
    </modal>
  </div>
</template>

<script setup>
import { marked } from "marked";
import DOMPurify from "dompurify";

import { computed } from "vue";

import Modal from "@/plugins/modal";

const emit = defineEmits(["update:showHelp"]);
const props = defineProps({
  description: {
    type: String,
    default: null,
  },
  limit: {
    type: Number,
    default: 0,
  },

  showHelp: {
    type: Boolean,
    default: false,
  },
});
const compiledMarkdown = computed(() => {
  if (props.description) {
    if (!props.limit) {
      return DOMPurify.sanitize(marked(props.description));
    } else {
      let desmin = props.description
        .split("\n")
        .slice(0, props.limit)
        .join("\n");
      return DOMPurify.sanitize(marked(desmin));
    }
  } else return "";
});

function hideHelp() {
  emit("update:showHelp", false);
}
</script>
