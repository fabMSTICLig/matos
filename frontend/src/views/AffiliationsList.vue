<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <input
            v-model="search_input"
            type="search"
            placeholder="Search"
          /><router-link
            class="btn btn-primary float-right"
            role="button"
            :to="{ name: 'affiliation', params: { affid: 'new' } }"
            >Ajouter</router-link
          >
        </div>
        <div class="card-body">
          <div class="table-responsive table-hover">
            <table class="table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Nom</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects_paginated"
                  :key="item.id"
                  v-on:click="selected_object = item"
                >
                  <td v-text="affiliation_types[item.type]"></td>
                  <td v-text="item.name"></td>
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            :total-pages="pages_count"
            :total="objects_filtered.length"
            :per-page="10"
            :current-page="current_page"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
    </div>
    <div class="col-12 col-md-6">
      <div class="card" v-if="selected_object">
        <div class="card-header">
          <h3 class="float-left" v-text="selected_object.name"></h3>
          <div class="btn-group float-right" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'affiliation',
                params: { affid: selected_object.id },
              }"
              >Modifier</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            Type : {{ affiliation_types[selected_object.type] }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ListMixin } from "@/common/mixins";
// @ is an alias to /src
import { mapGetters } from "vuex";
/*
  Vue liste Affiliations
*/
export default {
  name: "AffiliationList",
  mixins: [ListMixin],
  data() {
    return {
      search_fields: ["name"],
      ressource: "affiliations",
    };
  },
  computed: {
    ...mapGetters("affiliations", { affiliation_types: "types" }),
  },
  methods: {
    initComponent() {
      return this.$store.dispatch("affiliations/fetchTypes");
    },
  },
};
</script>
