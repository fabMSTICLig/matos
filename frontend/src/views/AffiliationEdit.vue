<template>
    <div class="row">
      <div class="col-12">
        <div class="card" v-if="object">
          <div class="card-header">
            <h3 v-text="cardName"></h3>
          </div>
          <div class="card-body">
            <form>
              <div class="form-row">
                <div class="col">
                  <div class="form-group"><label>Name</label><input v-model="object.name" class="form-control"
                      type="text"></div>
                  <div class="form-group"><label>Type</label>
                    <select class="form-control" v-model="object.type">
                        <option v-for="(typename,type) in affiliation_types" :value="type" v-text="typename" :key="type"></option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="btn-group" role="group">
                <button v-if="is_new" class="btn btn-primary" type="button" v-on:click="create">Ajouter</button>
                <button v-if="!is_new" class="btn btn-primary" type="button" v-on:click="update">Modifier</button>
                <button v-if="!is_new" class="btn btn-danger" type="button" v-on:click="destroy">Supprimer</button>
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
import {
  mapGetters
} from "vuex";
export default {
  name: "AffiliaionEdit",
  mixins: [EditMixin],
  data() {
    return {
      ressource: "affiliations",
      new_label: "Nouvelle Affiliation",
      object_name: "Affiliation",
    }
  },
  computed: {
    ...mapGetters("affiliations", {
      affiliation_types: "types"
    }),
  },
  methods: {
    get_empty(){
        return {
          type: Object.keys(this.affiliation_types)[0],
          name: ""
        }

    },
    make_label(){
        return this.object.name;
    },
    initComponent(){
        return this.$store.dispatch("affiliations/fetchTypes")
    },
  },
};
</script>
