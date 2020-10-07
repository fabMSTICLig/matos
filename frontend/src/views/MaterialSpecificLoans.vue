<template>
  <div>
    <div v-if="selected_object">
      <div class="row">
        <div class="col-12 col-md-12 col-lg-5">
          <div class="card">
            <div class="card-header input-group">
              <h5 style="margin-top: 7px; margin-right: 15px;">Instances</h5>
              <input type="text" class="form-control" value="Search" />
              <div class="">
                <router-link class="btn btn-primary float-left" role="button" :to="materialsRoute"
                  >Retour</router-link>
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
                    <tr v-for="item in objects_list"
                        :key="item.id"
                        v-on:click="setInstance(item)"
                        :class="{
                        'table-active':
                          selected_instance && item.id == selected_instance.id
                        }">
                      <td>{{ item.name }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- pagination -->
            </div>
          </div>
        </div>
        <div class="col-12 col-md-12 col-lg-7">
          <div class="card">
            <div class="card-header input-group">
              <h5 style="margin-top: 7px; margin-right: 15px;">Prêts</h5>
              <input
                class="form-control"
                v-model="search_input"
                type="text"
                placeholder="Search"
              />
              <div class="input-group-prepend">
                  <label class="input-group-text" for="typeselect">Ordre</label>
              </div>
                <select v-model="sort_input">
                  <option
                    v-for="item in sort_choices"
                    :value="item.value"
                    :key="item.value"
                    >{{ item.label }}</option>
                </select>
            </div>
            <div class="card-body">
              <form>
                <div class="form-row">
                  <div class="col">
                    <div class="table-responsive d-table table-hover">
                      <table class="table">
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
                          <tr v-for="loan in objects_paginated"
                            :key="loan.id"
                            v-on:click="selected_object = loan"
                            :class="{
                              'table-active':
                                selected_object && loan.id == selected_object.id
                            }">
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
                      v-if="objects_filtered.length"
                      :total-pages="pages_count"
                      :total="objects_filtered.length"
                      :per-page="per_page"
                      :current-page="current_page"
                      @pagechanged="onPageChange"
                    />
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { ListMixin } from "@/common/mixins";
import Vue from "vue";

export default {
  name: "MaterialSpecificLoans",
  mixins: [ListMixin],
  data() {
    return {
      selected_object: null,
      selected_instance: null,
      material: "",
      loaded: false,
      ressource: "entities/specificMaterials",
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" },
        return_date: { value: 3, label: "Date de retour" }
      },
    };
  },

  computed: {
    ...mapGetters({
      loans: "entities/specificMaterials/instances/loans",
      status: "loans/status",
      userById: "users/byId",
      users: "users/list"
    }),
    objects_filtered() {
        if(this.loans.length){
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
            if (this.sort_input == this.sort_choices.return_date.value){
              if (a.return_date && b.return_date) {
                return a.return_date.localeCompare(b.return_date);
              }
              if (a.return_date && !b.return_date) {
                return -1
              }
              if (b.return_date && !a.return_date) {
                return 1
              }
            }
            });
        }
        return this.loans;
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
    selectObject(item) {
      this.selected_instance = Object.assign({}, item);
    },
    setInstance(item) {
      this.selected_instance = Object.assign({}, item);
      this.$store
        .dispatch("entities/specificMaterials/instances/materialLoans", {
          id_entity: this.$route.params.entityid,
          id_specificmaterial: this.$route.params.matid,
          id_instance: this.selected_instance.id
        })
        .then((data) => {
          this.selected_object = this.objects_filtered[0];
          console.log(this.loans)
        })
    }
  },

  beforeMount() {
    var pall=[]
    pall.push(this.$store.dispatch("users/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));
    pall.push(this.$store
      .dispatch(this.ressource + "/fetchSingle", {
        id: this.$route.params.matid,
        prefix: this.prefix
      })
      .then(data => {
        this.material = data;
      }));
    pall.push( this.$store
      .dispatch("entities/specificMaterials/instances/fetchList", {
        prefix: this.instancePrefix
      })
      .then(() => {
        if (this.objects_list.length > 0) {
          this.selectObject(this.objects_list[0]);
        }
      }));
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
        })
    });

  }
};
</script>
