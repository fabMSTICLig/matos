<template>
  <div v-if="object">
    <fieldset v-if="!edited && object.infos" v-html="compiledMarkdown"></fieldset>
    <div id="editor" v-if="edited">
      <textarea :value="input" @input="update"></textarea>
        <div v-html="compiledMarkdown"></div>
        <button @click="markedInfos"
                class="btn btn-primary"
        >Valider</button>
    </div>
  </div>
</template>

<script>
import marked  from "marked";
import { debounce } from "vue-debounce";

export default {
  name: "Markdown",
  props: {
    object: {
      type: Object,
      required: true
    },
    edited: {
      type: Boolean,
      required: true
    },
    infos: {
      type: String
    }
  },
  data() {
    return {
      input: "### Informations",
      loaded_infos : false,
      syntax: ""
    };
  },
  computed: {

    compiledMarkdown() {      
      let md="";

      if(!this.edited) {
        if (localStorage.getItem("marked_entityInfos") != null) {
          md = localStorage.getItem("marked_entityInfos");
        }
      }
      else {
        md = this.input;
      }
     
      return marked(md, { sanitize: true }) ;
    },
  },
  watch: {
    
  },
  methods: {
    update(e) {
      debounce(this.input = e.target.value , 400)

      let entityInfos = this.input.split("### Informations")
      entityInfos = "### Informations " + entityInfos[1]
      localStorage.setItem(
        "marked_entityInfos",
        entityInfos
      );
    },

    markedInfos(){
      this.$emit('edited', !this.edited)
    },
  },

  beforeMount() {

    this.syntax = "# Titre niveau 1 à 6 ######"+"\n"+

"pour créer des paragraphes, revenir à la ligne"+" \n "+ "\n"+

"**texte en gras** *italique*"+" \n "+ 
  
  "`code`"+ " \n " + " \n" + " \n" +

"Mon site web [UFR](https://ufr-imag.univ-grenoble-alpes.fr)."+ " \n " + " \n" + " \n" +

"liste numerotée :"+ " \n " + " \n" + " \n" +
"1. élément" +  " \n " + " \n" + " \n" +
"2. élément" +" \n " + " \n" + " \n" +

"liste : "+" \n " + " \n" + " \n" + "* élément" + " \n " + " \n" + " \n" ;

    if (localStorage.getItem("marked_entityInfos") != null) {
      console.log("chargement")
      this.input = this.syntax
      this.input += localStorage.getItem("marked_entityInfos");
    }
    else {
      this.input = "";
      this.input += this.syntax
      this.input += this.infos;
    }

   
  }

};
</script>
<style scoped>

#editor {
  margin: 0;
  height: 100%;
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: #333;
}

textarea,
#editor div {
  display: inline-block;
  width: 49%;
  height: 100vh;
  vertical-align: top;
  box-sizing: border-box;
  padding: 0 20px;
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

</style>