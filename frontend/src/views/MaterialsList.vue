<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <input v-model="search_input" type="search" placeholder="Search" />

          <b-dropdown class="float-right" variant="primary" text="Ajouter">
            <b-dropdown-item
              :to="{ name: 'genericmaterial', params: { matid: 'new' } }"
              >Générique</b-dropdown-item
            >
            <b-dropdown-item
              :to="{ name: 'specificmaterial', params: { matid: 'new' } }"
              >Spécifique</b-dropdown-item
            >
          </b-dropdown>
        </div>
        <div class="card-body">
          <div class="table-responsive table-hover">
            <table class="table">
              <thead>
                <tr>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects_paginated"
                  :key="item.id + item.name"
                  v-on:click="selected_object = item"
                >
                  <td v-text="item.name"></td>
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            :total-pages="pages_count"
            :total="objects_filtered.length"
            :per-page="per_page"
            :current-page="current_page"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
    </div>
    <div class="col-12 col-md-6">
      <div class="card" v-if="selected_object">
        <div class="card-header">
          <h3 class="float-left">
            Matériel {{ isGeneric ? "Générique" : "Spécifique" }}
          </h3>
          <div class="btn-group float-right" role="group">
            <router-link class="btn btn-primary" role="button" :to="editRoute"
              >Modifier</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <h3>
            {{ selected_object.name }}
          </h3>
          <p class="card-text">
            {{ selected_object.description }}
          </p>
          <table class="table">
            <tr>
              <th scope="row">Ref interne</th>
              <td>{{ selected_object.ref_int }}</td>
            </tr>
            <tr>
              <th scope="row">Ref fabricant</th>
              <td>{{ selected_object.ref_man }}</td>
            </tr>
            <tr>
              <th scope="row">Localisation</th>
              <td>{{ selected_object.localisation }}</td>
            </tr>
            <tr v-if="isGeneric">
              <th scope="row">Quantité</th>
              <td>{{ selected_object.quantity }}</td>
            </tr>
          </table>
          <p>
            <span><strong>Tags :&nbsp;</strong></span>
            <DisplayIdList
              fieldName="tags"
              :object="selected_object"
              ressource="tags"
            />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ListMixin } from "@/common/mixins";
import DisplayIdList from "@/components/DisplayIdList";
export default {
  name: "MaterialsList",
  mixins: [ListMixin],
  components: {
    DisplayIdList
  },
  data() {
    return {
      search_fields: ["name"],
      ressource: "entities/genericMaterials"
    };
  },
  computed: {
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    },
    objects_list() {
      return this.$store.getters["entities/genericMaterials/list"]
        .concat(this.$store.getters["entities/specificMaterials/list"])
        .sort((a, b) => {
          if (a.name > b.name) return -1;
          if (a.name < b.name) return 1;
          return 0;
        });
    },
    isGeneric() {
      return "quantity" in this.selected_object;
    },
    editRoute() {
      var name = "specificmaterial";
      if ("quantity" in this.selected_object) {
        name = "genericmaterial";
      }
      return { name: name, params: { matid: this.selected_object.id } };
    }
  },
  methods: {
    initList() {
      this.$store
        .dispatch("entities/genericMaterials/fetchList", {
          prefix: this.prefix
        })
        .then(() => {
          this.$store
            .dispatch("entities/specificMaterials/fetchList", {
              prefix: this.prefix
            })
            .then(() => {
              if (this.objects_list.length > 0) {
                this.selected_object = this.objects_list[0];
              }
            });
        });
    }
  }
};
</script>
