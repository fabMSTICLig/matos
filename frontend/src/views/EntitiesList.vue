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
                  :class="{
                    'table-active':
                      selected_object && item.id == selected_object.id,
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
                params: { entityid: selected_object.id },
              }"
              v-show="isManager"
              >Modifier</router-link
            >
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'materialslist',
                params: { entityid: selected_object.id },
              }"
              v-show="isManager"
              >Matériels</router-link
            >
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'entityloans',
                params: { entityid: selected_object.id },
              }"
              v-show="isManager"
              >Prêts</router-link
            >
          </div>
        </div>
        <div class="card-body">
          <markdown
            :description="selected_object.description"
            :displayed="displayed"
          ></markdown>
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
import Markdown from "@/components/Markdown";
/*
  Vue Liste Entités
*/
export default {
  name: "EntitiesList",
  mixins: [ListMixin],
  components: {
    DisplayIdList,
    Markdown,
  },
  data() {
    return {
      ressource: "entities",
      displayed: true,
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
    },
  },
  methods: {
    search_fields(objects_list, search_input) {
      return objects_list
        .filter((item) => {
          return ["name"].some((field) => {
            return (
              item[field].toLowerCase().indexOf(search_input.toLowerCase()) > -1
            );
          });
        })
        .sort((a, b) => {
          var owna = this.authUser.entities.indexOf(a.id) > -1;
          var ownb = this.authUser.entities.indexOf(b.id) > -1;
          if (owna && !ownb) return -1;
          if (!owna && ownb) return 1;
          return 0;
        });
    },
    initList() {
      return this.$store
        .dispatch(this.ressource + "/fetchList", { prefix: this.prefix })
        .then(() => {
          if ("select" in this.$route.query) {
            var ent = this.$store.getters["entities/byId"](
              Number(this.$route.query["select"])
            );
            if (ent) this.selected_object = ent;
          } else if (this.objects_filtered.length > 0) {
            this.selected_object =
              this.objects_list[
                (this.current_page - 1) * process.env.VUE_APP_MAXLIST
              ];
          }
        });
    },
  },
};
</script>
