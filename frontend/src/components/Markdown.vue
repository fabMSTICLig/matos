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
      v-model="showhelp"
      >
      <h6>
        Utilisation de la syntaxe markdown pour modifier la description de
        l'entité :
      </h6>
      <h6>titre de niveau 1 à 6</h6>
      <p>
        # Titre 1
      </p>
      <p>
        ## Titre 2
      </p>
      <p>
        ### Titre 3
      </p>
      <p>
        ###### Titre 6
      </p>

      <h6>Paragraphes</h6>
      <p>Revenir à la ligne pour les paragraphes</p>
      <h6>Liens</h6>
      <p>[lien entité](https://lien-entité)</p>
      <p>lien avec référence</p>
      <span>[Utilisation d'un numero pour la référence d'un lien][1]</span>
      <p></p>
      <h6>Listes</h6>
      <i>Numerotée</i>
      <p>
        1. Element 2. Element
      </p>
      <i>à Puces</i>
      <p>* Element</p>
      <h6>Séparation</h6>
      <span>---</span>
      <h6>Citations</h6>
      <span> > Citations </span>
      <div class="center-btn">
        <button type="button" class="btn btn-info" @click="hideHelp">
          Ok
        </button>
      </div>
    </modal>
  </div>
</template>

<script>
import marked from "marked";
import DOMPurify from "dompurify";
import { debounce } from "vue-debounce";
import Modal from "@/components/Modal";

export default {
  name: "Markdown",
  props: {
    description: {
      type: String,
      required: true
    },
    displayed: {
      type: Boolean
    },
    showhelp: {
      type: Boolean
    }

  },
  components: {
    Modal
  },
  data() {
    return {
      loaded_infos: false,
      input: ""
    };
  },
  computed: {
    compiledMarkdown() {
      return DOMPurify.sanitize(marked(this.description));
    }
  },
  watch: {
    description(text) {
      debounce((this.input = text), 400);
    }
  },
  methods: {
    hideHelp(){
      this.$parent.$emit('hideHelp', false);
    }
  }
};
</script>
<style>
#markdown {
  margin: 0;
  height: 100%;
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: #333;
}

textarea,
#markdown div {
  display: inline-block;
  width: 100%;
  height: 50vh;
  vertical-align: top;
  box-sizing: border-box;
}

textarea {
  border: none;
  border-right: 1px solid #ccc;
  resize: none;
  outline: none;
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}

code {
  color: #f66;
}

#markdown h6 {
  color: #777 !important;
  margin-bottom: 0.5rem !important;
  margin-top: -0.375rem;
}

#markdown h4 {
  margin-bottom: 0.75rem;
  font-size: 1.5rem;
  font-family: "News Cycle", "Arial Narrow Bold", sans-serif;
  font-weight: 700;
  line-height: 1.1;
}

#markdown p {
  margin-top: 25px;
  margin-bottom: 1rem;
}

blockquote {
  background: #f9f9f9;
  border-left: 10px solid #ccc;
  margin: 1.5em 10px;
  padding: 1em 10px .1em 10px;
  quotes: "\201C""\201D""\2018""\2019";
}

#modal-syntaxe .modal {
  display: block !important;
}

#modal-syntaxe .modal-dialog {
  overflow-y: initial !important;
}
#modal-syntaxe .modal-body {
  height: 500px;
  overflow-y: auto;
}
#modal-syntaxe .center-btn {
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 15px;
  text-align: center;
}

#editor {
  margin: 30px 0px 30px 0px;
}
</style>
