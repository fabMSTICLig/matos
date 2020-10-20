<template>
  <div>
    <h2>{{ entityById($route.params.entityid) | field("name") }}</h2>
    <div class="row">
      <div class="col-12 col-md-6">
        <div class="card">
          <div class="card-header">
            <div class="form form-inline">
              <div class="form-group mr-2">
                <input
                  class="form-control"
                  v-model="search_input"
                  type="search"
                  placeholder="Search"
                />
              </div>
              <div class="form-group">
                <label class="mr-1">Ordre : </label>
                <select class="form-control" v-model="sort_input">
                  <option
                    v-for="item in sort_choices"
                    :value="item.value"
                    :key="item.value"
                    >{{ item.label }}</option
                  >
                </select>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="table-responsive table-hover">
              <table class="table">
                <thead>
                  <tr>
                    <th>Utilisateur</th>
                    <th>Status</th>
                    <th>Date sortie</th>
                    <th>Date retour prévue</th>
                    <th>Date retour</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in objects_paginated"
                    :key="item.id"
                    v-on:click="selected_object = item"
                    :class="{
                      'table-active':
                        selected_object && item.id == selected_object.id
                    }"
                  >
                    <td>
                      {{ userById(item.user) | field("username") }}
                    </td>
                    <td v-text="loan_status[item.status]"></td>
                    <td v-text="item.checkout_date"></td>
                    <td v-text="item.due_date"></td>
                    <td v-text="item.return_date"></td>
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
            <button class="btn btn-primary"
              role="button"
              @click="copy=true"
            >Copier</button>
            <div class="btn-group float-right" role="group">
              <button
                class="btn btn-primary"
                role="button"
                @click="editLoan(selected_object)"
                :disabled="copy"
              >
                Modifier
              </button>
              <button
                class="btn btn-danger"
                role="button"
                @click="destroyLoan(selected_object)"
                :disabled="copy"
              >
                Supprimer
              </button>
            </div>
          </div>
          <div class="card-body">
            <form class="form" v-if="copy && copyObj" @submit="copyLoan">
              <div class="form-row">
                <div class="col-md-6 form-group">
                  <label>Date sortie :</label>
                  <input
                    class="form-control"
                    type="date"
                    v-model="copyObj.checkout_date"
                    required
                  />
                </div>
              </div>
              <div class="form-row">
                <div class="col-md-6 form-group">
                  <label>Utilisateur :</label>
                  <input-datalist
                    v-model="copyObj.user"
                    ressource="users"
                    :makeLabel="makeUserLabel"
                  ></input-datalist>
                </div>
              </div>
              <div class="form-row">
                <div class="col-md-12 form-group">
                  <div class="table-responsive-md">
                    <table class="table">
                      <thead>
                        <tr class="d-flex">
                          <th class="col-8">Matériels</th>
                          <th class="col-3">Quantité</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          class="d-flex"
                          v-for="item in copyObj.generic_materials"
                          :key="'g' + item.material"
                        >
                          <td class="col-8">
                            {{ gmById(item.material) | field("name") }}
                          </td>
                          <td class="col-3">
                            <input
                              type="number"
                              class="number-input form-control form-control"
                              v-model="item.quantity"
                            />
                          </td>
                        </tr>
                        <tr
                          class="d-flex"
                          v-for="item in copyObj.models"
                          :key="'s' + item"
                        >
                          <td class="col-11" colspan="2">
                            {{ smById(item) | field("name") }}
                            <div>
                              <h6>Instances</h6>
                              <DynList
                                :ressource="specificinstances[item]"
                                v-model="copyObj.specific_materials"
                                v-if="specificinstances[item]"
                              ></DynList>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn btn-primary float-left">Valider</button>
              <button @click="copy=false" class="btn btn-primary float-left">Annuler</button>
            </form>
            <table class="table" v-if="!copy">
              <tr>
                <th scope="row">Utilisateur</th>
                <td>
                  {{ userById(selected_object.user) | field("username") }}
                </td>
              </tr>
              <tr>
                <th scope="row">Status</th>
                <td>{{ loan_status[selected_object.status] }}</td>
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

            <h5 v-if="!copy">Commentaires</h5>
            <p class="card-text">
              {{ selected_object.comments }}
            </p>

            <h5 v-if="!copy">Matériels</h5>
            <ul class="list-group" v-if="!copy">
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
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { mapGetters } from "vuex";
import { ListMixin } from "@/common/mixins";
import { showMsgConfirm } from "@/components/Modal";
import InputDatalist from "@/components/InputDatalist";
import DynList from "@/components/DynList";
import { DataHelper } from "@/common/helpers";

export default {
  name: "EntityLoansList",
  mixins: [ListMixin],
  data() {
    return {
      ressource: "loans",
      loaded: false,
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" },
        return_date: { value: 3, label: "Date de retour" }
      },
      copy: false,
      specificinstances: {},
      copyObj: {}
    };
  },
  components: {
    InputDatalist,
    DynList
  },
  props: ["entityid"],
  computed: {
    ...mapGetters("loans", { loan_status: "status" }),
    ...mapGetters(["authUser"]),
    ...mapGetters({
      gmById: "genericmaterials/byId",
      smById: "specificmaterials/byId",
      userById: "users/byId",
      entityById: "entities/byId",
      users: "users/list"
    }),
    objects_filtered() {
      var filtered = this.objects_list
        .filter(item => {
          return item.entity == this.$route.params.entityid;
        })
        .filter(item => {
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
          if (a.checkout_date.localeCompare(b.checkout_date) > 0) {
            return a.checkout_date.localeCompare(b.checkout_date)
          };
          if (a.checkout_date.localeCompare(b.checkout_date) == 0) {
            return a.due_date.localeCompare(b.due_date)
          };
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
  },
  watch: {
    entityid: function() {
      this.selected_object = this.objects_filtered[0];
    },
    selected_object: function(){
      console.log(DataHelper)
      this.copyObj = DataHelper.copy(this.selected_object);
      this.selected_object.models.forEach(item => {
        this.initInstances(item);
      })
    }
  },
  methods: {
    initComponent() {
      return this.$store.dispatch("loans/fetchStatus");
    },
    initInstances(item) {
      return this.$store
        .dispatch("specificmaterials/instances/fetchList", {
          prefix: "specificmaterials/" + item + "/"
        })
        .then(data => {
          Vue.set(this.specificinstances, item, data);
        });
    },
    editLoan(loan) {
      this.$store.commit("loans/setPending", loan);
      this.$router.push({ name: "loan" });
    },
    destroyLoan(item) {
      showMsgConfirm("Voulez vous vraiment supprimer ce prêt ?").then(value => {
        if (value)
          this.$store.dispatch("loans/destroy", { id: item.id }).then(() => {
            if (this.objects_filtered.length > 0) {
              this.selected_object = this.objects_filtered[0];
            }
          });
      });
    },
    makeUserLabel(item) {
      return item.username;
    },
    copyLoan(){
      this.$store
        .dispatch("loans/copy", { id: this.copyObj.id, data: this.copyObj })
        .then(() => {
          this.copy = !this.copy;
        });
    }
  },

  beforeMount() {
    var pall = [];
    pall.push(this.$store.dispatch("specificmaterials/fetchList"));
    pall.push(this.$store.dispatch("genericmaterials/fetchList"));
    pall.push(this.$store.dispatch("users/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));

    Promise.all(pall).then(() => {
      this.loaded = true;
    });
  }
};
</script>
