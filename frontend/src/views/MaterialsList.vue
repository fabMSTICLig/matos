<template>
  <div class="row">
    <div class="col-12 col-md-12 col-lg-6">
      <div class="card">
        <div class="card-header input-group">
          <input
            class="form-control"
            v-model="search_input"
            type="search"
            placeholder="Search"
          />
          <div class="input-group-prepend">
            <label class="input-group-text" for="typeselect">Type</label>
          </div>
          <select v-model="type_input">
            <option value="1">Les deux</option>
            <option value="2">Generique</option>
            <option value="3">Specifique</option>
          </select>
          <div class="input-group-append">
            <Dropdown
              :items="newmaterialroutes"
              label="Ajouter"
              classtoogle="btn-primary"
              :button="true"
            />
          </div>
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
                  :class="{
                    'table-active':
                      selected_object &&
                      item.id + item.name ==
                        selected_object.id + selected_object.name
                  }"
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
    <div class="col-12 col-md-12 col-lg-6">
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
          <markdown
            :description="selected_object.description"
            :displayed="displayed"
          ></markdown>
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
import Dropdown from "@/components/Dropdown";
import Markdown from "@/components/Markdown";

export default {
  name: "MaterialsList",
  mixins: [ListMixin],
  components: {
    DisplayIdList,
    Dropdown,
    Markdown
  },
  data() {
    return {
      type_input: 1,
      search_fields: ["name"],
      ressource: "entities/genericMaterials",
      newmaterialroutes: [
        {
          to: { name: "genericmaterial", params: { matid: "new" } },
          label: "Générique"
        },
        {
          to: { name: "specificmaterial", params: { matid: "new" } },
          label: "Spécifique"
        }
      ],
      displayed: true
    };
  },
  computed: {
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    },
    objects_list() {
      if (this.type_input == 2)
        return this.$store.getters["entities/genericMaterials/list"];
      else if (this.type_input == 3)
        return this.$store.getters["entities/specificMaterials/list"];
      else {
        if (this.$store.getters["entities/specificMaterials/list"])
          return this.$store.getters["entities/genericMaterials/list"]
            .concat(this.$store.getters["entities/specificMaterials/list"])
            .sort((a, b) => {
              if (a.name > b.name) return -1;
              if (a.name < b.name) return 1;
              return 0;
            });
        else return [];
      }
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
