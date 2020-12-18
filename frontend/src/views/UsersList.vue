<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <input v-model="search_input" type="search" placeholder="Search" />
        </div>
        <div class="card-body">
          <div class="table-responsive table-hover">
            <table class="table">
              <thead>
                <tr>
                  <th>Nom utilisateur</th>
                  <th>Prénom</th>
                  <th>Nom</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects_paginated"
                  :key="item.id"
                  v-on:click="selected_object = item"
                >
                  <td v-text="item.username"></td>
                  <td v-text="item.first_name"></td>
                  <td v-text="item.last_name"></td>
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
          <h3 class="float-left" v-text="selected_object.username"></h3>
          <div class="btn-group float-right" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{ name: 'user', params: { userid: selected_object.id } }"
              >Modifier</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            <span
              ><strong>{{ selected_object.username }} :&nbsp;</strong></span
            >{{ selected_object.first_name }} {{ selected_object.last_name }}
          </p>
          <p>
            <span><strong>Email :&nbsp;</strong></span
            ><a :href="'mailto:' + selected_object.email">{{
              selected_object.email
            }}</a>
          </p>
          <h5>Affiliations</h5>
          <DisplayIdList
            fieldName="affiliations"
            :object="selected_object"
            ressource="affiliations"
          />
          <h5>Entities</h5>
          <DisplayIdList
            fieldName="entities"
            :object="selected_object"
            ressource="entities"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DisplayIdList from "@/components/DisplayIdList";
import { ListMixin } from "@/common/mixins";
/*
  Vue liste Utilisateurs
*/
export default {
  name: "UsersList",
  mixins: [ListMixin],
  components: {
    DisplayIdList
  },
  data() {
    return {
      search_fields: ["username", "first_name", "last_name"],
      ressource: "users"
    };
  }
};
</script>
