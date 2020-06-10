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
              <div class="col col-12">
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
                    <label>Référence interne</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.ref_int"
                    />
                  </div>
                  <div class="form-group">
                    <label>Référence fabriquant</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.ref_man"
                    />
                  </div>
                  <div class="form-group">
                    <label>Description</label
                    ><textarea
                      class="form-control"
                      v-model="object.description"
                    />
                  </div>
                  <div class="form-group">
                    <label>Localisation</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.localisation"
                    />
                  </div>
                  <div class="form-group">
                    <label>Quantité</label
                    ><input
                      class="form-control"
                      type="number"
                      v-model="object.quantity"
                    />
                  </div>
                  <div class="form-group">
                    <label>Tags</label>
                    <TagsInput
                      fieldName="tags"
                      :object="object"
                      ressource="tags"
                    />
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
import TagsInput from "@/components/TagsInput";
export default {
  name: "GenericMaterialEdit",
  mixins: [EditMixin],
  components: {
    TagsInput
  },
  data() {
    return {
      ressource: "entities/genericMaterials",
      new_label: "Nouvel Matériel Générique",
      object_name: "Matériel"
    };
  },
  computed: {
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    }
  },
  methods: {
    get_empty() {
      return {
        name: "",
        ref_int: null,
        ref_man: null,
        localisation: null,
        description: "",
        quantity: 0,
        entity: this.$route.params["entityid"],
        tags: []
      };
    },
    make_label() {
      return this.object.name;
    }
  }
};
</script>
