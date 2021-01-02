<template>
  <div>
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
            <div class="col col-md-6 col-lg-6 col-xs-10 col-sm-12">
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
                  <label>Contact</label
                  ><input
                    class="form-control"
                    type="email"
                    v-model="object.contact"
                    required
                  />
                </div>
                <div class="form-group">
                  <label>Description</label>
                  <textarea
                    class="form-control"
                    v-model="object.description"
                  ></textarea>
                  <a href="#" @click.prevent="showMessage">Aide</a>
                </div>
              </fieldset>
            </div>

            <div class="md col-12 col-md-6 col-lg-6">
              <markdown
                :description="object.description"
                :showhelp="showHelp"
                @hideHelp="showHelp = false"
              ></markdown>
            </div>

            <div class="col col-12 col-md-6">
              <fieldset>
                <legend>Managers</legend>
                <div class="form-group">
                  <DynList
                    options="users"
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
            <div class="col col-12 col-md-6">
              <fieldset>
                <legend>Affiliations</legend>
                <div class="form-group">
                  <DynList
                    options="affiliations"
                    v-model="object.affiliations"
                  ></DynList>
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
              v-on:click="update(msg)"
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
  </div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
import DynList from "@/components/DynList";
import Markdown from "@/components/Markdown";

/*
  Vue Edition d'une Entité
*/
export default {
  name: "EntityEdit",
  mixins: [EditMixin],
  components: {
    DynList,
    Markdown
  },
  data() {
    return {
      ressource: "entities",
      new_label: "Nouvelle Entité",
      object_name: "Entité",
      showHelp: false,
      msg: "mise à jour"
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
    showMessage() {
      this.showHelp = true;
    }
  }
};
</script>
