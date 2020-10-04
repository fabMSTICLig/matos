<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 class="float-left" v-text="object.name"></h3>
          <div role="group" class="btn-group float-right">
            <button
              class="btn btn-primary"
              type="button"
              @click="addMaterial(object)"
            >
              Ajouter
            </button>
          </div>
        </div>
        <div class="card-body">
          <markdown
            :description="object.description"
            :displayed="displayed"
          ></markdown>
          <table class="table">
            <tr>
              <th scope="row">Ref interne</th>
              <td>{{ object.ref_int }}</td>
            </tr>
            <tr>
              <th scope="row">Ref fabricant</th>
              <td>{{ object.ref_man }}</td>
            </tr>
          </table>

          <p>
            <span><strong>Tags :&nbsp;</strong></span>
            <DisplayIdList fieldName="tags" :object="object" ressource="tags" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Markdown from "@/components/Markdown";

import { mapGetters, mapMutations } from "vuex";
export default {
  name: "MaterialInfos",
  components: {
    Markdown
  },

  data() {
    return {
      object: null,
      ressource: "",
      object_name: "Matériel",
      displayed: true
    };
  },
  computed: {
    ...mapGetters({
      tags: "tags/list",
      pending_loan: "loans/pending_loan"
    }),
    materialTags() {
      return this.tags.filter(item => {
        return this.object["tags"].includes(item.id);
      });
    }
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial"
    }),
    make_label() {
      return this.object.name;
    }
  },
  beforeMount() {
    this.$store.dispatch("tags/fetchList");

    if (this.$route.name == "specificmaterial-item") {
      this.ressource = "specificmaterials";
    }
    if (this.$route.name == "genericmaterial-item") {
      this.ressource = "genericmaterials";
    }
    if (parseInt(this.$route.params[this.$route.meta.routeparam], -1) != -1) {
      this.$store
        .dispatch(this.ressource + "/fetchSingle", {
          id: this.$route.params[this.$route.meta.routeparam]
        })
        .then(data => {
          this.object = Object.assign({}, data);
        });
    }
  }
};
</script>
