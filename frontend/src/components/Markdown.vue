<template>
  <div>
    <div id="editor">
        <div class="card" v-if="!displayed">
          <div class="card-body">
            <div v-html="compiledMarkdown" :value="input" id="markdown"></div>
          </div>
        </div>
        <div v-html="compiledMarkdown" :value="input" v-if="displayed" id="markdown"></div>
    </div>
  </div>
</template>

<script>
import marked  from "marked";
import { debounce } from "vue-debounce";

export default {
  name: "Markdown",
  props: {
    description: {
      type: String,
      required: true
    },
    displayed: {
      type: Boolean
    }
  },
  data() {
    return {
      loaded_infos : false,
      syntax: "",
      input:""
    };
  },
  computed: {

    compiledMarkdown() {      
      return marked(this.description, { sanitize: true }) ;
    },
  },
  watch: {
    description(text){
      
      debounce(this.input = text , 400)

    }
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

       
  }

};
</script>
<style>

#markdown {
  margin: 0;
  height: 100%;
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: #333
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
</style>