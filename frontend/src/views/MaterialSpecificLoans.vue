<template>
  <div>
    <div v-if="selected_object">
      <div class="row">
        <div class="col-12 col-md-12 col-lg-7 col-sm-12">
          <div class="card">
            <div class="card-header input-group">
              <div class="input-group-append">
                <div
                  :class="show ? 'dropdown show' : 'dropdown'"
                  @focusout="hide"
                  style="margin-right: 10px;"
                >
                  <div
                    class="btn btn-primary dropdown-toggle"
                    id="dropdownMenuButton"
                    @click="toogle"
                  >
                    Instances
                  </div>
                  <div
                    :class="show ? 'dropdown-menu show' : 'dropdown-menu'"
                    :id="'tooltip' + _uid"
                    aria-labelledby="dropdownMenuButton"
                  >
                    <button
                      class="dropdown-item"
                      v-for="item in objects_list"
                      :key="item.id"
                      @click="selectInstance(item)"
                      type="button"
                    >
                      {{ item.name }}
                    </button>
                  </div>
                </div>
              </div>
              <input
                type="search"
                class="form-control"
                v-model="search_input"
                placeholder="Search"
              />

              <div class="input-group-prepend">
                <label class="input-group-text" for="typeselect">Ordre</label>
              </div>
              <select v-model="sort_input" class="form-control">
                <option
                  v-for="item in sort_choices"
                  :value="item.value"
                  :key="item.value"
                  >{{ item.label }}</option
                >
              </select>
            </div>
            <div class="card-body">
              <div class="table-responsive table-hover">
                <table class="table" v-if="objects_filtered">
                  <thead>
                    <tr>
                      <th>Utilisateur</th>
                      <th>Status</th>
                      <th>Date de sortie</th>
                      <th>Date de retour prévue</th>
                      <th>Date de retour</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="loan in loans_paginated"
                      :key="loan.id"
                      v-on:click="selected_object = loan"
                      :class="{
                        'table-active':
                          selected_object && loan.id == selected_object.id
                      }"
                    >
                      <td>
                        {{ userById(loan.user) | field("username") }}
                      </td>
                      <td>{{ status[loan.status] }}</td>
                      <td>{{ loan.checkout_date }}</td>
                      <td>{{ loan.due_date }}</td>
                      <td>{{ loan.return_date }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <pagination
                v-if="loans.length"
                :total-pages="pages_total()"
                :total="loans.length"
                :per-page="per_page"
                :current-page="current_page"
                @pagechanged="onPageChange"
              />
            </div>
          </div>
        </div>
        <div class="col-12 col-md-12 col-lg-5 col-sm-12">
          <div class="card" v-if="selected_object">
            <div class="card-header">
              <h3 class="float-left" v-text="selected_object.name"></h3>
              <router-link
                class="btn btn-primary float-left"
                role="button"
                :to="materialsRoute"
                >Retour</router-link
              >
              <div class="btn-group float-right" role="group">
                <button
                  class="btn btn-primary"
                  role="button"
                  @click="editLoan(selected_object)"
                >
                  Modifier
                </button>
                <button
                  class="btn btn-dark"
                  role="button"
                  @click="deleteLoan()"
                  v-if="isRemoval"
                >
                  Supprimer
                </button>
              </div>
            </div>
            <div class="card-body">
              <table class="table">
                <tr>
                  <th scope="row">Status</th>
                  <td>{{ status[selected_object.status] }}</td>
                </tr>
                <tr>
                  <th scope="row">Date sortie</th>
                  <td>{{ selected_object.checkout_date }}</td>
                </tr>
                <tr>
                  <th scope="row">Date retour prévue</th>
                  <td>{{ selected_object.due_date }}</td>
                </tr>
                <tr>
                  <th scope="row">Date retour</th>
                  <td>{{ selected_object.return_date }}</td>
                </tr>
              </table>

              <h5>Commentaires</h5>
              <p class="card-text">
                {{ selected_object.comments }}
              </p>

              <h5>Matériels</h5>
              <ul class="list-group">
                <li
                  class="list-group-item"
                  v-for="item in selected_object.models"
                  :key="'s' + item"
                >
                  {{ smById(item) | field("name") }}
                </li>
                <li
                  class="list-group-item"
                  v-for="item in selected_object.generic_materials"
                  :key="'g' + item.material"
                >
                  {{ gmById(item.material) | field("name") }}
                </li>
              </ul>
            </div>
          </div>
          <modal
            id="modal-delete"
            title="Voulez vous vraiment supprimer ce prêt ?"
            v-model="showDelete"
            hideFooter
          >
            <p>
              Confirmer la suppression du prêt
            </p>

            <div>
              <div
                class="btn-group"
                role="group"
                aria-label="Voulez vous vraiment supprimer ce prêt ?"
              >
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="destroyLoan(selected_object)"
                >
                  Oui
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="showDelete = false"
                >
                  Non
                </button>
              </div>
            </div>
          </modal>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Pagination from "@/components/Pagination";
import Modal from "@/components/Modal";

export default {
  name: "MaterialSpecificLoans",
  data() {
    return {
      selected_object: null,
      selected_instance: null,
      search_input: "",
      current_page: 1,
      material: "",
      loaded: false,
      ressource: "entities/specificMaterials",
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" },
        return_date: { value: 3, label: "Date de retour" }
      },
      show: false,
      showDelete: false
    };
  },
  components: {
    Pagination,
    Modal
  },
  computed: {
    ...mapGetters({
      loans: "entities/specificMaterials/instances/loans",
      status: "loans/status",
      userById: "users/byId",
      users: "users/list",
      gmById: "genericmaterials/byId",
      smById: "specificmaterials/byId"
    }),
    objects_filtered() {
      if (this.loans.length) {
        var filtered = this.loans.filter(item => {
          var user = this.userById(item.user);
          if (user)
            return (
              user.username
                .toLowerCase()
                .indexOf(this.search_input.toLowerCase()) > -1
            );
          else return true;
        });
        return filtered.sort((a, b) => {
          if (this.sort_input == this.sort_choices.due_date.value)
            return a.due_date.localeCompare(b.due_date);
          if (this.sort_input == this.sort_choices.checkout_date.value)
            return a.checkout_date.localeCompare(b.checkout_date);
          if (this.sort_input == this.sort_choices.return_date.value) {
            if (a.return_date && b.return_date) {
              return a.return_date.localeCompare(b.return_date);
            }
            if (a.return_date && !b.return_date) {
              return -1;
            }
            if (b.return_date && !a.return_date) {
              return 1;
            }
          }
        });
      }
      return this.loans;
    },
    isRemoval() {
      return this.selected_object.status == 2;
    },
    loans_paginated() {
      return this.objects_filtered.slice(
        (this.current_page - 1) * process.env.VUE_APP_MAXLIST,
        this.current_page * process.env.VUE_APP_MAXLIST
      );
    },
    per_page() {
      return parseInt(process.env.VUE_APP_MAXLIST);
    },
    objects_list() {
      return this.$store.getters["entities/specificMaterials/instances/list"];
    },
    instancePrefix() {
      return (
        "entities/" +
        this.$route.params.entityid +
        "/specificmaterials/" +
        this.$route.params.matid +
        "/"
      );
    },
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    },
    materialsRoute() {
      var name = "materialslist";
      return { name: name, params: { entityid: this.$route.params.entityid } };
    }
  },
  methods: {
    selectInstance(item) {
      this.selected_instance = Object.assign({}, item);
      this.show = false;
      this.$store
        .dispatch("entities/specificMaterials/instances/materialLoans", {
          id_entity: this.$route.params.entityid,
          id_specificmaterial: this.$route.params.matid,
          id_instance: this.selected_instance.id
        })
        .then(() => {
          this.selected_object = this.objects_filtered[0];
          console.log(this.loans);
        });
    },
    setInstance(item) {
      this.selected_instance = Object.assign({}, item);
    },

    toogle(e) {
      e.preventDefault();
      this.show = !this.show;
    },
    hide(e) {
      if (!this.$el.contains(e.relatedTarget)) {
        this.show = false;
      }
    },
    pages_total() {
      return Math.ceil(this.loans.length / process.env.VUE_APP_MAXLIST);
    },
    onPageChange(page) {
      this.current_page = page;
    },
    editLoan(loan) {
      this.$store.commit("loans/setPending", loan);
      this.$router.push({ name: "loan" });
    },
    destroyLoan(item) {
      this.$store.dispatch("loans/destroy", { id: item.id }).then(() => {
        if (this.objects_filtered.length > 0) {
          this.selected_object = this.objects_filtered[0];
        }
      });
    },
    deleteLoan() {
      this.showDelete = true;
    }
  },
  beforeMount() {
    var pall = [];
    pall.push(this.$store.dispatch("specificmaterials/fetchList"));
    pall.push(this.$store.dispatch("genericmaterials/fetchList"));
    pall.push(this.$store.dispatch("users/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));
    pall.push(
      this.$store
        .dispatch(this.ressource + "/fetchSingle", {
          id: this.$route.params.matid,
          prefix: this.prefix
        })
        .then(data => {
          this.material = data;
        })
    );
    pall.push(
      this.$store
        .dispatch("entities/specificMaterials/instances/fetchList", {
          prefix: this.instancePrefix
        })
        .then(() => {
          if (this.objects_list.length > 0) {
            this.selectInstance(this.objects_list[0]);
          }
        })
    );
    Promise.all(pall).then(() => {
      this.$store
        .dispatch("entities/specificMaterials/instances/materialLoans", {
          id_entity: this.$route.params.entityid,
          id_specificmaterial: this.$route.params.matid,
          id_instance: this.selected_instance.id
        })
        .then(() => {
          this.selected_object = this.objects_filtered[0];
          this.loaded = true;
        });
    });
  }
};
</script>
