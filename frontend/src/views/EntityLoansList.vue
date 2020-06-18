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
                  >
                    <td>{{ userById(item.user) | field("username") }}</td>
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
            <div class="btn-group float-right" role="group">
              <button
                class="btn btn-primary"
                role="button"
                @click="editLoan(selected_object)"
              >
                Modifier
              </button>
              <button
                class="btn btn-danger"
                role="button"
                @click="destroyLoan(selected_object)"
              >
                Supprimer
              </button>
            </div>
          </div>
          <div class="card-body">
            <table class="table">
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
      </div>
    </div>
  </div>
</template>

<script>
import { ListMixin } from "@/common/mixins";
// @ is an alias to /src
import { mapGetters } from "vuex";
export default {
  name: "LoansList",
  mixins: [ListMixin],
  data() {
    return {
      ressource: "loans",
      loaded: false,
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" }
      }
    };
  },
  computed: {
    ...mapGetters("loans", { loan_status: "status" }),
    ...mapGetters(["authUser"]),
    ...mapGetters({
      gmById: "genericmaterials/byId",
      smById: "specificmaterials/byId",
      userById: "users/byId",
      entityById: "entities/byId"
    }),
    isEditable() {
      return (
        this.selected_object.status == 1 || this.selected_object.status == 2
      );
    },
    objects_filtered() {
      var filtered = this.objects_list
        .filter(item => {
          return item.entity == this.$route.params.entityid;
        })
        .filter(item => {
            var user = this.userById(item.user)
            if(user)
              return user
                .username.toLowerCase()
                .indexOf(this.search_input.toLowerCase()) > -1
            else return true
        });
      return filtered.sort((a, b) => {
        if (a.return_date && !b.return_date) return 1;
        if (b.return_date && !a.return_date) return -1;
        if (this.sort_input == this.sort_choices.due_date.value)
          return a.due_date.localeCompare(b.due_date);
        if (this.sort_input == this.sort_choices.checkout_date.value)
          return a.due_date.localeCompare(b.checkout_date);
      });
    }
  },
  methods: {
    initComponent() {
      return this.$store.dispatch("loans/fetchStatus");
    },
    editLoan(loan) {
      this.$store.commit("loans/setPending", loan);
      this.$router.push({ name: "loan" });
    },
    destroyLoan(item) {
      this.$bvModal.msgBoxConfirm("Voulez vous vraiment supprimer ce prêt ?").then((value)=>{
            if(value)this.$store.dispatch("loans/destroy", {'id':item.id});
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
