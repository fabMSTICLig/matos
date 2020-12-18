<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <input v-model="search_input" type="search" placeholder="Search" />
          <div class="btn-group float-right" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{ name: 'tag', params: { tagid: 'new' } }"
              >Ajouter</router-link
            ><button
              type="button"
              class="btn btn-danger"
              title="Supprimer les tags inutilisés"
              @click="destroyUnused"
            >
              Nettoyer
            </button>
          </div>
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
                name: 'tag',
                params: { tagid: selected_object.id }
              }"
              >Modifier</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            {{ selected_object.name }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ListMixin } from "@/common/mixins";
import { showMsgConfirm } from "@/components/Modal";
// @ is an alias to /src

/*
  Vue liste des Tags
*/
export default {
  name: "TagList",
  mixins: [ListMixin],
  data() {
    return {
      search_fields: ["name"],
      ressource: "tags"
    };
  },
  methods: {
    destroyUnused() {
      showMsgConfirm(
        "Voulez vous vraiment supprimer tout les tags non utilisés ?"
      ).then(val => {
        if (val) this.$store.dispatch("tags/destroyUnused");
      });
    }
  }
};
</script>
