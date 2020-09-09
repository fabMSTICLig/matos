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
                <div role="group" class="btn-group"><button class="btn btn-primary" type="button" style="height: 37px;">Ajouter</button></div>
                </div>
                <div>
                    <span class="icon-link">&#10138;</span>
                </div>
                <div v-show="bookmark">
                  <sup style="font-size: 19px;">{{linkMaterial}}</sup></div>
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

import {mapGetters} from "vuex";
export default {
  name: "GenericMaterial",
  mixins: [EditMixin],
  components: {
    Markdown
  },

  data() {
    return {
      ressource: "genericmaterials",
      object_name: "Matériel",
      activeDset: true,
      displayed: true,
      bookmark: false

    };
  },
  computed: {
    ...mapGetters({
      tags: "tags/list"
     }),
    materialTags(){
      return this.tags.filter(item => {
        return this.object["tags"].includes(item.id);
      });
    },
    linkMaterial(){
      return process.env.VUE_APP_SERVER + " /" + this.$route.fullpath
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
        tags: []
      };
    },
    make_label() {
      return this.object.name;
    },
    getLink() {
      this.bookmark = true
    }
  },
  beforeMount() {
    this.$store.dispatch("tags/fetchList");
  }
};
</script>
<style>
  .tags {
    margin-bottom: 25px;
    margin-top: 15px;
  }

  .icon-link {
    color: #EB6864;
    border: 1px solid #EB6864;
    border-radius: 5px;
  }

</style>