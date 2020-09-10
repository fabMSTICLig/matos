<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 v-text="cardName"></h3>
        </div>
        <div class="card-body">
          <form id="editor-form">
            <div class="row">
              <div class="col col-12">
                <div class="d-flex justify-content-between">
                    <div><span class="badge badge-info text-capitalize" style="font-size: 14px;">Détails</span>
                </div>
                <div role="group" class="btn-group"><button class="btn btn-primary" type="button" style="height: 37px;" @click="toLoan">Ajouter</button></div>
                </div>
   
                <div class="col col-12 col-md-6">
                   <markdown :description="object.description" :displayed="displayed"></markdown>
                </div>               
                <div class="d-flex flex-row flex-fill justify-content-between align-items-start align-content-center flex-wrap" style="width: auto;max-width: 470px;">
                    <div class="d-block justify-content-start align-items-start align-content-start" style="width: auto;"><span><strong>Fabriquant</strong></span><span style="margin-left: 26px;">{{object.ref_man}}</span></div>
                </div>
              </div>
              <div class="tags col">
                <ul class="list-group list-group-horizontal d-flew flex-wrap">
                  <li
                    class="list-group-item border rounded"
                    v-for="item in materialTags"
                    :key="item.id"
                  >{{item.name}}</li>
                </ul>
              </div>
            </div>
           </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { EditMixin } from "@/common/mixins";
import Markdown from "@/components/Markdown";

import {mapGetters, mapMutations} from "vuex";
export default {
  name: "GenericMaterial",
  mixins: [EditMixin],
  components: {
    Markdown
  },

  data() {
    return {
      object_name: "Matériel",
      activeDset: true,
      displayed: true,
    };
  },
  computed: {
    ...mapGetters({
      tags: "tags/list",
      pending_loan: "loans/pending_loan"

     }),
    materialTags(){
      return this.tags.filter(item => {
        return this.object["tags"].includes(item.id);
      });
    }
   
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial"
    }),
    get_empty() {
      return {
        name: "",
        ref_int: null,
        ref_man: null,
        localisation: null,
        description: "",
        quantity: 0,
        tags: []
      };
    },
    make_label() {
      return this.object.name;
    },
  
    toLoan() {
      if(this.pending_loan.generic_materials.length){
        this.addMaterial(this.object);      
      }
      else {
        console.log(this.pending_loan)
        this.addMaterial(this.object);
      }     
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
  }
};
</script>
<style>
  .tags {
    margin-bottom: 25px;
    margin-top: 15px;
  }
</style>