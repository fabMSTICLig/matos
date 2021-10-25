<template>
  <div>
    <div id="editor">
      <div class="card" v-if="!displayed">
        <div class="card-body">
          <div v-html="compiledMarkdown" :value="input" id="markdown"></div>
        </div>
      </div>
      <div
        v-html="compiledMarkdown"
        :value="input"
        v-if="displayed"
        id="markdown"
      ></div>
    </div>
    <modal
      id="modal-syntaxe"
      title="Markdown Syntaxe"
      hideFooter
      v-bind:show="showhelp"
      @change="hideHelp()"
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
      <p></p>
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
        <button type="button" class="btn btn-info" @click="hideHelp">Ok</button>
      </div>
    </modal>
  </div>
</template>

<script>
import marked from "marked";
import DOMPurify from "dompurify";
import { debounce } from "vue-debounce";
import Modal from "@/components/Modal";
/* 
Utilisation de la librairie marked et de la dépendance vue-debounce
Composant pour afficher le markdown compilé du texte passé en propriété
*/
export default {
  name: "Markdown",
  props: {
    description: {
      type: String,
    },
    displayed: {
      type: Boolean,
    },
    showhelp: {
      type: Boolean,
    },
  },
  components: {
    Modal,
  },
  data() {
    return {
      loaded_infos: false,
      input: "",
    };
  },
  computed: {
    compiledMarkdown() {
      if (this.description) return DOMPurify.sanitize(marked(this.description));
      else return "";
    },
  },
  watch: {
    description(text) {
      debounce((this.input = text), 400);
    },
  },
  methods: {
    hideHelp() {
      this.$emit("hideHelp");
    },
  },
};
</script>
