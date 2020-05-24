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
            :to="{ name: 'entityedit', params: { entityid: 'new' } }"
            v-if="authUser.is_staff"
            >Ajouter</router-link
          >
        </div>
        <div class="card-body">
          <div class="table-responsive table-hover">
            <table class="table">
              <thead>
                <tr>
                  <th>Nom</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects_paginated"
                  :key="item.id"
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
                name: 'entityedit',
                params: { entityid: selected_object.id }
              }"
              v-show="isManager"
              >Edit</router-link
            >
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'materialslist',
                params: { entityid: selected_object.id }
              }"
              v-show="isManager"
              >Materials</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            {{ selected_object.description }}
          </p>
          <p class="card-text">
            <span><strong>Contact :&nbsp;</strong></span
            ><a :href="'mailto:' + selected_object.contact">{{
              selected_object.contact
            }}</a>
          </p>
          <h5>Affiliations</h5>
          <DisplayIdList
            fieldName="affiliations"
            :object="selected_object"
            ressource="affiliations"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { ListMixin } from "@/common/mixins";
import DisplayIdList from "@/components/DisplayIdList";
export default {
  name: "EntitiesList",
  mixins: [ListMixin],
  components: {
    DisplayIdList
  },
  data() {
    return {
      search_fields: ["name"],
      ressource: "entities"
    };
  },
  computed: {
    ...mapGetters(["authUser"]),
    isManager() {
      return (
        (this.selected_object &&
          this.authUser.entities.indexOf(this.selected_object.id) > -1) ||
        this.authUser.is_staff
      );
    }
  },
  methods: {}
};
</script>
