<template>
  <div>
    <h1>Rechercher</h1>
    <div class="row">
      <div class="col-xl-3">
        <div class="card">
          <div class="card-header">
            <h4>Filtres</h4>
          </div>
          <div class="card-body">
            <form class="form">
              <div class="form-group">
                <label>Chercher</label
                ><input
                  type="search"
                  class="form-control"
                  placeholder="Arduino"
                  v-model="search_input"
                  v-debounce:400ms="refreshSearch"
                />
              </div>
              <div class="form-group">
                <label>Type</label>
                <select class="form-control" v-model="type_input">
                  <option value="">Les deux</option>
                  <option value="g">Generique</option>
                  <option value="s">Specifique</option>
                </select>
              </div>

              <div class="form-group">
                <label>Entités</label>
                <TagsInput
                  :list="entities_filter"
                  v-on:add="entities_filter.push($event)"
                  v-on:remove="$removeFromArray(entities_filter, $event)"
                  ressource="entities"
                  forbidAdd
                />
              </div>

              <div class="form-group">
                <label>Tags</label>
                <TagsInput
                  :list="tags_filter"
                  v-on:add="tags_filter.push($event)"
                  v-on:remove="$removeFromArray(tags_filter, $event)"
                  ressource="tags"
                  forbidAdd
                />
              </div>
              <div
                v-if="isAdmin || authUser.entities.length"
                class="form-group custom-control custom-switch"
              >
                <input
                  type="checkbox"
                  class="custom-control-input"
                  v-model="hidden"
                  id="check-active"
                />
                <label class="custom-control-label" for="check-active"
                  >Invisible</label
                >
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            <pagination
              :total-pages="pages_count"
              :total="objects_list.length"
              :per-page="10"
              :current-page="current_page"
              @pagechanged="onPageChange"
            />
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="item in objects_list"
                :key="item.name + item.id"
                class="
                  list-group-item list-group-item-action
                  flex-column
                  align-items-start
                "
              >
                <div class="d-flex w-100 justify-content-between">
                  <a href="#" @click.prevent="goToMaterial(item)"
                    ><h4>{{ item.name }}</h4></a
                  >
                  <strong
                    ><router-link
                      :to="{
                        name: 'entityinfos',
                        params: { entityid: item.entity },
                      }"
                      >{{ getEntityName(item.entity) }}</router-link
                    ></strong
                  >
                </div>
                <markdown
                  :description="item.description"
                  :displayed="displayed"
                ></markdown>
                <p>
                  <strong>Tags :</strong>
                  <DisplayIdList
                    fieldName="tags"
                    :object="item"
                    ressource="tags"
                    :autoload="false"
                  />
                </p>

                <button
                  class="btn btn-primary wt-1"
                  type="button"
                  @click="addItem(item)"
                  :class="{
                    disabled:
                      pending_loan.entity && pending_loan.entity != item.entity,
                  }"
                  title="Les matériels d'un prêt doivent tous appartenir à la même entité"
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
import Markdown from "@/components/Markdown";
/*
  Vue recherche et ajout de matériel au prêt courant
  permet l'accès à la vue d'un matériel
*/

export default {
  name: "Search",
  components: {
    TagsInput,
    Pagination,
    DisplayIdList,
    Markdown,
  },
  data() {
    return {
      search_input: "",
      type_input: "",
      tags_filter: [],
      hidden: false,
      current_page: 1,
      count: 0,
      per_page: process.env.VUE_APP_MAXLIST,
      entities_filter: [],
      genericmaterials: [],
      specificmaterials: [],
      displayed: true,
    };
  },
  computed: {
    ...mapGetters({
      entities: "entities/list",
      entityById: "entities/byId",
      authUser: "authUser",
      isAdmin: "isAdmin",
      pending_loan: "loans/pending_loan",
    }),

    objects_list() {
      return this.genericmaterials.concat(this.specificmaterials);
    },
    pages_count() {
      return Math.ceil(this.count / process.env.VUE_APP_MAXLIST);
    },
    search_change() {
      return (
        this.type_input, this.hidden, this.tags_filter, this.entities_filter
      );
    },
    query_params() {
      return {
        params: {
          limit: this.per_page,
          offset: (this.current_page - 1) * this.per_page,
          type: this.type_input,
          search: this.search_input,
          entities: this.entities_filter.join(),
          tags: this.tags_filter.join(),
          hidden: this.hidden,
        },
      };
    },
  },
  watch: {
    search_change() {
      this.current_page = 1;
      this.refreshSearch();
    },
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial",
    }),
    goToMaterial(item) {
      if (item.instances) {
        this.$router.push({
          name: "specificmaterialitem",
          params: { matid: item.id },
        });
      } else {
        this.$router.push({
          name: "genericmaterialitem",
          params: { matid: item.id },
        });
      }
    },
    addItem(item) {
      if (this.pending_loan.entity == null) {
        this.entities_filter.push(item.entity);
      }
      this.addMaterial(item);
    },
    onPageChange(page) {
      this.current_page = page;
      this.refreshSearch();
    },
    getEntityName(id) {
      var entity = this.entityById(id);
      if (entity) return entity.name;
      else return "";
    },
    refreshSearch() {
      this.$store
        .dispatch("materials/searchMaterials", this.query_params)
        .then((data) => {
          this.count = data.count;
          this.genericmaterials = data.results.generic_materials;
          this.specificmaterials = data.results.specific_materials;
        });
    },
  },
  beforeMount() {
    this.$store.dispatch("entities/fetchList");
    /* 
      Si le prêt courant est en readonly (ajout de materiel impossible) on le reset
      Vérification utilisateur non manager d'une entité
    */
    if (
      !this.isAdmin &&
      this.authUser.entities.indexOf(this.pending_loan.entity) == -1 &&
      (this.pending_loan.status == 3 || this.pending_loan.status == 4)
    ) {
      this.$store.commit("loans/resetPending");
    } else {
      if (this.pending_loan.entity != null) {
        this.entities_filter.push(this.pending_loan.entity);
      }
    }
    this.refreshSearch();
  },
};
</script>
