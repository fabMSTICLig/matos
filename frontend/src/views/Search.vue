<template>
  <div>
    <h1>Recherche</h1>
    <div class="row">
      <div class="col-xl-3">
        <div>
          <h4>Filtres</h4>
        </div>
        <form class="form">
          <div class="form-group">
            <label>Chercher</label
            ><input type="search" class="form-control" v-model="search_input" />
          </div>
          <div class="form-group">
            <label>Type</label>
            <select class="form-control" v-model="type_input">
              <option value="1">Les deux</option>
              <option value="2">Generique</option>
              <option value="3">Specifique</option>
            </select>
          </div>

          <div class="form-group">
            <label>Entités</label>
            <TagsInput
              fieldName="entities_filter"
              :object="this"
              ressource="entities"
              forbidAdd
            />
          </div>

          <div class="form-group">
            <label>Tags</label>
            <TagsInput
              fieldName="tags"
              :object="this"
              ressource="tags"
              forbidAdd
            />
          </div>
        </form>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            <form class="form form-inline">
              <div class="form-group">
                <label class="mr-1" >Ordre : </label>
                <select class="form-control" v-model="sort_input">
                  <option
                    v-for="item in sort_choices"
                    :value="item.value"
                    :key="item.value"
                    >{{ item.label }}</option
                  >
                </select>
              </div>
            </form>

            <pagination
              :total-pages="pages_count"
              :total="objects_filtered.length"
              :per-page="10"
              :current-page="current_page"
              @pagechanged="onPageChange"
            />
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="item in objects_paginated"
                :key="item.name + item.id"
                class="list-group-item list-group-item-action flex-column align-items-start"
              >
                <div class="d-flex w-100 justify-content-between">
                  <h4>{{ item.name }}</h4>
                  <strong>{{ getEntityName(item.entity) }}</strong>
                </div>
                <p class="text-truncate">{{ item.description }}</p>
                <p>
                  <strong>Tags :</strong>
                  <DisplayIdList
                    fieldName="tags"
                    :object="item"
                    ressource="tags"
                  />
                </p>
                <button
                  class="btn btn-primary wt-1"
                  type="button"
                  @click="addMaterial(item)"
                  :class="{
                    disabled:
                      pending_loan.entity && pending_loan.entity != item.entity
                  }"
                  title="Les matériel d'un prêt doivent tous appartenir à la même entité"
                >
                  Ajouter
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapMutations } from "vuex";
import TagsInput from "@/components/TagsInput";
import Pagination from "@/components/Pagination";
import DisplayIdList from "@/components/DisplayIdList";
export default {
  name: "Search",
  components: {
    TagsInput,
    Pagination,
    DisplayIdList
  },
  data() {
    return {
      search_input: "",
      sort_input: 1,
      type_input: 1,
      tags: [],
      current_page: 1,
      entities_filter: [],
      sort_choices: {
        name: { value: 1, label: "Nom" },
        entity: { value: 2, label: "Entité" }
      }
    };
  },
  computed: {
    ...mapGetters({
      entities: "entities/list",
      genericmaterials: "genericmaterials/list",
      specificmaterials: "specificmaterials/list",
      entityById: "entities/byId",
      authUser: "authUser",
      isAdmin: "isAdmin",
      pending_loan: "loans/pending_loan"
    }),
    objects_list() {
      if (this.type_input == 2) return this.genericmaterials;
      else if (this.type_input == 3) return this.specificmaterials;
      else {
        if (this.genericmaterials)
          return this.genericmaterials
            .concat(this.specificmaterials)
            .sort((a, b) => {
              if (a.name > b.name) return -1;
              if (a.name < b.name) return 1;
              return 0;
            });
        else return [];
      }
    },
    objects_filtered() {
      var filtered = this.objects_list.filter(item => {
        var filterstring = ["name", "ref_int", "ref_man"].some(field => {
          if (item[field] == null) return false;
          return (
            item[field].toLowerCase().indexOf(this.search_input.toLowerCase()) >
            -1
          );
        });
        var entitycheck = true;
        if (filterstring && this.entities_filter.length != 0) {
          entitycheck = this.entities_filter.indexOf(item.entity) > -1;
        }
        var tagcheck = true;
        if (filterstring && this.tags.length != 0 && entitycheck) {
          tagcheck = this.tags.some(tag => item.tags.indexOf(tag) > -1);
        }
        return filterstring && entitycheck && tagcheck;
      });
      return filtered.sort((a, b) => {
        if (this.sort_input == this.sort_choices.name.value)
          return a.name.localeCompare(b.name);
        if (this.sort_input == this.sort_choices.entity.value)
          return this.entityById(a.entity).name.localeCompare(
            this.entityById(b.entity).name
          );
      });
    },
    objects_paginated() {
      return this.objects_filtered.slice(
        (this.current_page - 1) * process.env.VUE_APP_MAXLIST,
        this.current_page * process.env.VUE_APP_MAXLIST
      );
    },
    pages_count() {
      return Math.ceil(
        this.objects_filtered.length / process.env.VUE_APP_MAXLIST
      );
    }
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial"
    }),
    onPageChange(page) {
      this.current_page = page;
    },
    getEntityName(id) {
      var entity = this.entityById(id);
      if (entity) return entity.name;
      else return "";
    }
  },
  beforeMount() {
    this.$store.dispatch("specificmaterials/fetchList");
    this.$store.dispatch("genericmaterials/fetchList");
    this.$store.dispatch("entities/fetchList");
    //Si le prêt courant est en readonly (ajout de materiel impossible) on le reset
    if(
        !this.isAdmin &&
        this.authUser.entities.indexOf(this.pending_loan.entity) == -1 &&
        (this.pending_loan.status == 3 || this.pending_loan.status == 4)
    ) {
      this.$store.commit("loans/resetPending");
    }
  }
};
</script>
