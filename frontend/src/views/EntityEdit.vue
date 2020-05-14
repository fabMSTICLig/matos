<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 v-text="cardName"></h3>
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
    </div>
  </div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
import DynList from "@/components/DynList";
export default {
  name: "EntityEdit",
  mixins: [EditMixin],
  components: {
    DynList
  },
  data() {
    return {
      ressource: "entities",
      new_label: "Nouvelle Entité",
      object_name: "Entité"
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
    }
  }
};
</script>
