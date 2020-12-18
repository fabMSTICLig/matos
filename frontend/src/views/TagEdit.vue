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
              <div class="col">
                <div class="form-group">
                  <label>Name</label
                  ><input
                    v-model="object.name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
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
  </div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
// @ is an alias to /src

/*
  Edition d'un Tag 
*/
export default {
  name: "TagEdit",
  mixins: [EditMixin],
  data() {
    return {
      ressource: "tags",
      new_label: "Nouveau Tag",
      object_name: "Tag",
      msg: "mis à jour"
    };
  },
  computed: {},
  methods: {
    get_empty() {
      return {
        name: ""
      };
    },
    make_label() {
      return this.object.name;
    }
  }
};
</script>
