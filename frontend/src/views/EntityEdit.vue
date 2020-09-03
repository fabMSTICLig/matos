<template>
  <div class="col-12">
    <div class="card" v-if="object">
      <div class="card-header">
        <h3 class="float-left" v-text="cardName"></h3>
        <div v-if="!is_new" class="btn-group float-right" role="group">
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'materialslist',
              params: { entityid: object.id }
            }"
            >Matériels</router-link
          >
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'entityloans',
              params: { entityid: object.id }
            }"
            >Prêts</router-link
          >
        </div>
      </div>
      <div class="card-body">
        <form id="editor-form">
          <div class="form-row">
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
                <legend>Informations</legend>
                <div class="form-group">
                  <label>Nom</label
                  ><input
                    class="form-control"
                    type="text"
                    v-model="object.name"
                    required
                  />
                </div>
                <div class="form-group">
                  <label>Description</label
                  ><textarea
                    class="form-control"
                    v-model="object.description"
                  ></textarea>
                  <markdown :description="object.description"></markdown>
                </div>
                <div class="form-group">
                  <label>Contact</label
                  ><input
                    class="form-control"
                    type="email"
                    v-model="object.contact"
                    required
                  />
                </div>
              </fieldset>
            </div>
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
                <legend>Affiliations</legend>
                <div class="form-group">
                  <DynList
                    ressource="affiliations"
                    v-model="object.affiliations"
                  ></DynList>
                </div>
              </fieldset>
            </div>
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
                <legend>Managers</legend>
                <div class="form-group">
                  <DynList
                    ressource="users"
                    v-model="object.managers"
                    :makeLabel="makeManagerLabel"
                  >
                    <template v-slot:default="slotProps">
                      <strong>@{{ slotProps.item.username }} :</strong>
                      {{ slotProps.item.first_name }}
                      {{ slotProps.item.last_name }}
                    </template>
                  </DynList>
                </div>
              </fieldset>
            </div>
          </div>
          <div class="btn-group" role="group">
            <button
              v-if="is_new"
              class="btn btn-primary"
              type="button"
              v-on:click="create"
            >
              Ajouter
            </button>
            <button
              v-if="!is_new"
              class="btn btn-primary"
              type="button"
              v-on:click="update"
            >
              Modifier
            </button>
            <button
              v-if="!is_new"
              class="btn btn-danger"
              type="button"
              v-on:click="destroy"
            >
              Supprimer
            </button>
          </div>
        </form>
      </div>
    </div>
    <modal id="modal-syntaxe" title="Markdown Syntaxe" hideFooter v-model="showMD">
      <h6>Utilisation de la syntaxe markdown pour modifier la description de l'entité : </h6>   
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
        1. Element
        2. Element
      </p>
      <i>à Puces</i>
      <p>* Element</p>
      <h6>Séparation</h6>
      <span>---</span>
      <h6>Citations</h6>
      <span> > Citations </span>
      <div>
          <button
            type="button"
            class="btn btn-info"
            @click="infoMD"            
          >
            Ok
          </button>
        </div>
    </modal>
  </div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
import DynList from "@/components/DynList";
import Markdown from "@/components/Markdown";
import { Modal } from "@/components/Modal";

export default {
  name: "EntityEdit",
  mixins: [EditMixin],
  components: {
    DynList,
    Markdown,
    Modal
  },
  data() {
    return {
      ressource: "entities",
      new_label: "Nouvelle Entité",
      object_name: "Entité",
      showMD: false
    };
  },
  computed: {},
  methods: {
    get_empty() {
      return {
        name: "",
        description: "",
        contact: "",
        affiliations: [],
        managers: []
      };
    },
    make_label() {
      return this.object.name;
    },
    makeManagerLabel(item) {
      return item.first_name + " " + item.last_name;
    },
    infoMD() {
      localStorage.setItem("syntax_md", true)
      this.showMD = false
    }
  },
  mounted() {
    if (localStorage.getItem("syntax_md") == null) {
      this.showMD = true;
    }
  }
};
</script>
<style>
  .form-group textarea {
    height: 261px;
  }

  .modal{
    display: block !important; 
  }

  .modal-dialog{
      overflow-y: initial !important
  }
  .modal-body{
      height: 500px;
      overflow-y: auto;
  }

  #modal-syntaxe button {
    margin-top: 15px;
    margin-bottom: 10px;
  }
</style>