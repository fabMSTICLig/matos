<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <h3>Mes prêts</h3>
        </div>
        <div class="card-body">
          <div class="table-responsive table-hover">
            <table class="table">
              <thead>
                <tr>
                  <th>Entité</th>
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
                  <td>{{ entityById(item.entity) | field("name") }}</td>
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
              {{ isEditable ? "Modifier" : "Consulter" }}
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
              <th scope="row">Entité</th>
              <td>{{ entityById(selected_object.entity) | field("name") }}</td>
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
      <modal
        id="modal-delete"
        title="Annuler demande de prêt"
        v-model="showDelete"
        hideFooter
      >
        <h6>Annuler la demande de prêt</h6>

        <p>
          Confirmer l'annulation de la demande de prêt
        </p>

        <div>
          <div class="btn-group" role="group" aria-label="Supprimer la demande">
            <button
              type="button"
              class="btn btn-primary"
              @click="validDestroy(selected_object)"
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
</template>

<script>
import { ListMixin } from "@/common/mixins";
import Modal from "@/components/Modal";
// @ is an alias to /src
import { mapGetters } from "vuex";
export default {
  name: "LoansList",
  mixins: [ListMixin],
  components: {
    Modal
  },
  data() {
    return {
      ressource: "loans",
      loaded: false,
      showDelete: false,
    };
  },
  computed: {
    ...mapGetters("loans", { loan_status: "status" }),
    ...mapGetters(["authUser"]),
    ...mapGetters({
      gmById: "genericmaterials/byId",
      smById: "specificmaterials/byId",
      entityById: "entities/byId"
    }),
    isManager() {
      return (
        (this.selected_object &&
          this.authUser.entities.indexOf(this.selected_object.entity) > -1) ||
        this.authUser.is_staff
      );
    },
    isEditable() {
      return (
        this.selected_object.status == 1 || this.selected_object.status == 2
      );
    },
    isRemoval() {
      return this.selected_object.status == 2 && !this.isManager;
    }
  },
  methods: {
    initComponent() {
      return this.$store.dispatch("loans/fetchStatus");
    },
    search_fields(list) {
      return list.filter(item => {
        return item.user == this.authUser.id;
      });
    },
    validDestroy(item) {
      this.$store
        .dispatch("loans/destroy", {
          data: item,
          id: item.id
        })
        .then(() => {
          this.$store.commit("loans/resetPending");
          if (this.objects_filtered.length > 0) {
            this.selected_object = this.objects_filtered[0];
          }
          this.showDelete=false;
          this.errors = [];
        })
        .catch(e => {
          if ("non_field_errors" in e.response.data) {
            this.errors = e.response.data.non_field_errors;
          }
          console.log(e.response);
        });
    },
    editLoan(item) {
      this.$store.commit("loans/setPending", item);
      this.$router.push({ name: "loan" });
    },
    deleteLoan() {
      this.showDelete = true;
    }
  },
  beforeMount() {
    var pall = [];
    pall.push(this.$store.dispatch("specificmaterials/fetchList"));
    pall.push(this.$store.dispatch("genericmaterials/fetchList"));
    pall.push(this.$store.dispatch("entities/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));
    Promise.all(pall).then(() => {
      this.loaded = true;
    });
  }
};
</script>
