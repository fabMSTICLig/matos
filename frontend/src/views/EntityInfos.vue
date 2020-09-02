<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 class="float-left">
            {{ object | field("name") }}
          </h3>
          <div class="btn-group float-right" role="group" aria-label="Basic example">
            <router-link
            class="btn btn-primary float-right"
            role="button"
            :to="{
              name: 'entitieslist'
            }"
            v-if="isManager"
            >Retour</router-link
            >
            <button @click="markedInfos"
                        v-if="isManager && !edited"
                        class="btn btn-primary float-right"

            >Modifier</button>
          </div>
         
        </div>
        <div class="card-body" v-show="loaded_infos">
          <fieldset v-if="!edited && !object.infos">
            <legend>Informations</legend>
            <p class="card-text">
              <span
                ><strong>{{ object.description }}</strong></span
              >
            </p>
            <p class="card-text">
              <span><strong>Contact :&nbsp;</strong></span
              ><a :href="'mailto:' + object.contact">{{ object.contact }}</a>
            </p>
            <h4>Affiliations :&nbsp;</h4>
            <DisplayIdList
              fieldName="affiliations"
              :object="object"
              ressource="affiliations"
              @setIdList="setIdList($event)"
            />
          </fieldset>
          <markdown :object="object" :edited="edited" v-if="loaded_infos" @edited="stateInfos($event)" :infos="input"></markdown>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import DisplayIdList from "@/components/DisplayIdList";
import Markdown from "@/components/Markdown";

export default {
  name: "Entity",
  data() {
    return {
      object: null,
      ressource: "entities",
      input: "### Informations",
      affiliations: "",
      edited: false,
      loaded_infos : false
    };
  },
  components: {
    DisplayIdList,
    Markdown
  },
  computed: {
    ...mapGetters(["authUser"]),
    isManager() {
      return (
        (this.object && this.authUser.entities.indexOf(this.object.id) > -1) ||
        this.authUser.is_staff
      );
    },
  },
  methods: {
  
    setIdList(evt) {      
      for(let i=0; i<=evt.length -1; i++) {
            this.affiliations += evt[i].name + " "
      }
      
      if (localStorage.getItem("marked_entityInfos") == null) {
        this.input = this.input + " \n" + this.object.description + "\n" + "##### Contact : "+  this.object.contact + "\n" + "##### Affiliations" + "\n" + "\n "+ this.affiliations;
      }

      if (localStorage.getItem("marked_entityInfos") != null) {
            let md = localStorage.getItem("marked_entityInfos");
            this.object.infos = md;
            this.input = md;
      } 
      
      this.loaded_infos = true;
    },

    markedInfos(){
      this.edited = !this.edited;
    },

    stateInfos(evt) {
      this.edited=evt;
    }
       
  },
 
  beforeMount() {
    if (
      this.$route.params[this.$route.meta.routeparam] != "new" &&
      parseInt(this.$route.params[this.$route.meta.routeparam], -1) != -1
    ) {
      this.$store
        .dispatch(this.ressource + "/fetchSingle", {
          id: this.$route.params[this.$route.meta.routeparam]
        })
        .then(data => {
          this.object = Object.assign({}, data);

        })    
    }
  }
};
</script>
