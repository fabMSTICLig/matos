<template>
  <div v-if="loaded">
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-header">
            <h4 class="float-left">{{ title }}</h4>
            <div class="btn-group float-right" role="group">
              <router-link
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'entityloans',
                  params: { entityid: pending_loan.entity },
                }"
                v-if="updateMode && canManage"
                >Retour entité</router-link
              >
              <router-link
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'authloans',
                }"
                v-if="updateMode && !canManage"
                >Mes prêts</router-link
              >
            </div>
          </div>
          <div class="card-body">
            <ul class="text-danger" v-show="errors.length != 0">
              <li
                v-for="error in errors"
                :key="error"
                v-text="error"
                tabIndex="-1"
              ></li>
            </ul>
            <form class="form" @submit="submitLoan">
              <div class="form-row">
                <div class="col-12 col-md-5 col-lg-5">
                  <div class="form-group" v-if="canManage">
                    <label>Utilisateur :</label>
                    <multiselect
                      v-model="loanUser"
                      placeholder="Selectionner un utilisateur"
                      :options="users"
                      track-by="id"
                      label="name"
                      :searchable="true"
                      :loading="usersLoading"
                      :internal-search="false"
                      :allow-empty="true"
                      select-label=""
                      :custom-label="makeUserLabel"
                      @search-change="searchUser"
                    >
                      <span slot="noResult"
                        >Pas de résultat. Modifier la recherche (3 lettres
                        min)</span
                      >
                      <span slot="noOptions"
                        >Veuillez taper au moins 3 lettres</span
                      >
                    </multiselect>

                    <!-- <input-datalist
                      v-model="pending_loan.user"
                      ressource="users"
                      :makeLabel="makeUserLabel"
                    ></input-datalist>-->
                  </div>
                  <div class="form-group">
                    <label>Entité :</label>
                    <input
                      type="text"
                      class="form-control"
                      :value="entityById(pending_loan.entity) | field('name')"
                      readonly
                    />
                  </div>
                  <div class="form-group">
                    <label>Status :</label>
                    <select
                      class="form-control"
                      v-model="pending_loan.status"
                      :disabled="!canManage"
                    >
                      <option
                        v-for="(val, key) in status"
                        v-text="val"
                        :key="key"
                        :value="key"
                      ></option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Date sortie :</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.checkout_date"
                      required
                      :disabled="readOnly"
                    />
                  </div>
                  <div class="form-group">
                    <label>Date retour prévue:</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.due_date"
                      required
                      :disabled="readOnly"
                    />
                  </div>
                  <div class="form-group" v-if="canManage">
                    <label>Date retour:</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.return_date"
                    />
                  </div>

                  <div class="form-group">
                    <label>Commentaire :</label>
                    <textarea
                      class="form-control"
                      v-model="pending_loan.comments"
                      :disabled="readOnly"
                    ></textarea>
                  </div>
                </div>
                <div class="col-12 col-md-7">
                  <p class="text-danger" v-show="emptyLoan">
                    Votre prêt doit contenir au moins un matériel. Pour un
                    materiel spécifique veuillez choisir une instance
                  </p>

                  <div class="table-responsive-md">
                    <table class="table">
                      <thead>
                        <tr class="d-flex">
                          <th class="col-8">Matériels</th>
                          <th class="col-3">Quantité</th>
                          <th class="col-1"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          class="d-flex"
                          v-for="item in pending_loan.generic_materials"
                          :key="'g' + item.material"
                        >
                          <td class="col-8 disabled">
                            {{ gmById(item.material) | field("name") }}
                          </td>
                          <td class="col-3 disabled">
                            <input
                              type="number"
                              min="1"
                              max="10000"
                              class="number-input form-control form-control"
                              v-model="item.quantity"
                              :disabled="readOnly"
                            />
                          </td>

                          <td class="col-1 disabled">
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              @click="removeMaterial(gmById(item.material))"
                              style="margin-left: -10px"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                        <tr
                          class="d-flex"
                          v-for="item in pending_loan.models"
                          :key="'s' + item"
                        >
                          <td class="col-11" colspan="2">
                            {{ smById(item) | field("name") }}
                            <div>
                              <h6>Instances</h6>
                              <DynList
                                v-if="item in specificinstances"
                                :options="specificinstances[item]"
                                v-model="pending_loan.specific_materials"
                                :readonly="readOnly"
                                :make-label="makeLabelInstance"
                              ></DynList>
                            </div>
                          </td>

                          <td>
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              @click="removeMaterial(smById(item))"
                              style="margin-left: -10px"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div
                    class="form-group"
                    v-if="
                      updateMode &&
                      (pending_loan.child ||
                        pending_loan.parent ||
                        pending_loan.status == 3)
                    "
                  >
                    <label>Historique :</label>
                    <div class>
                      <div role="group" class="btn-group">
                        <button
                          v-if="updateMode && pending_loan.parent"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pending_loan.parent)"
                        >
                          Précédent
                        </button>
                        <button
                          v-if="
                            updateMode &&
                            canManage &&
                            !pending_loan.child &&
                            pending_loan.status == 3
                          "
                          class="btn btn-info"
                          type="button"
                          @click="makeChild"
                        >
                          Créer un successeur
                        </button>

                        <button
                          v-if="updateMode && pending_loan.child"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pending_loan.child)"
                        >
                          Suivant
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12">
                <div role="group" class="btn-group">
                  <button
                    class="btn btn-primary float-left"
                    type="submit"
                    v-if="!readOnly"
                  >
                    {{ updateMode ? "Modifier" : labelSubmit }}
                  </button>
                  <button
                    class="btn btn-danger float-left"
                    type="button"
                    v-if="updateMode && !canManage && !readOnly"
                    @click="cancelLoan"
                  >
                    Annuler la demande
                  </button>
                  <button
                    class="btn btn-danger float-left"
                    type="button"
                    v-if="updateMode && canManage"
                    @click="destroyLoan"
                  >
                    Supprimer
                  </button>

                  <button
                    v-if="!updateMode"
                    class="btn btn-danger"
                    type="button"
                    @click="cleanMaterials"
                  >
                    Vider
                  </button>
                </div>
                <div role="group" class="btn-group float-right">
                  <button
                    v-if="updateMode"
                    class="btn btn-danger"
                    type="button"
                    @click="newLoan"
                  >
                    Nouveau prêt
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import Multiselect from "vue-multiselect";
import { mapGetters, mapMutations } from "vuex";
import DynList from "@/components/DynList";
import { showMsgOk } from "@/components/Modal";
/*
  Composant permettant de gérer le prêt courant
*/
export default {
  name: "Loan",
  components: {
    DynList,
    Multiselect,
  },
  props: ["loanid"],
  data() {
    return {
      loaded: false,
      usersLoading: false,
      errors: [],
    };
  },
  computed: {
    ...mapGetters({
      users: "users/list",
      userById: "users/byId",
      gmById: "materials/gmById",
      smById: "materials/smById",
      smiById: "materials/smiById",
      entityById: "entities/byId",
      loanById: "loans/byId",
      pending_loan: "loans/pending_loan",
      status: "loans/status",
      authUser: "authUser",
      isAdmin: "isAdmin",
    }),
    loanMessageSent() {
      if (this.pending_loan.status == 2) return "La demande a été envoyée";
      if (this.pending_loan.status == 3) return "La demande a été acceptée";
      if (this.pending_loan.status == 4) return "La demande a été refusée";
      if (this.pending_loan.status == 1) return "La demande a été annulée";

      return "La demande a été envoyée";
    },
    labelSubmit() {
      if (this.canManage && !this.updateMode) {
        return "Créer";
      } else {
        return "Envoyer la demande";
      }
    },
    loanUser: {
      get() {
        if (this.pending_loan.user) {
          return this.userById(this.pending_loan.user);
        } else return null;
      },
      set(val) {
        if (val) this.pending_loan.user = val.id;
        else this.pending_loan.user = null;
      },
    },
    emptyLoan() {
      return (
        this.pending_loan.generic_materials.length == 0 &&
        this.pending_loan.specific_materials.length == 0
      );
    },
    specificinstances() {
      let ret = {};
      this.pending_loan.models.forEach((id) => {
        ret[id] = [];
        let sm = this.smById(id);
        sm.instances.forEach((iid) => {
          let ins = this.smiById(iid);
          if (!ins.active && !this.canManage) ins.$isDisabled = true;
          ret[id].push(ins);
        });
      });
      return ret;
    },
    emptyInstances() {
      let ret = true;
      this.pending_loan.models.forEach((m) => {
        ret &= this.specificinstances[m].some((el) =>
          this.pending_loan.specific_materials.includes(el.id)
        );
      });
      return !ret;
    },
    canManage() {
      return (
        this.isAdmin ||
        this.authUser.entities.indexOf(this.pending_loan.entity) > -1
      );
    },
    updateMode() {
      return "id" in this.pending_loan;
    },
    readOnly() {
      return !this.canManage && this.pending_loan.status != 2;
    },
    title() {
      return this.readOnly
        ? "Consulter prêt"
        : this.updateMode
        ? "Modification prêt"
        : "Nouveau prêt";
    },

    checkDates() {
      /*
        Vérification des dates remplies pour la demande ou la modification 
      */
      return (
        (this.pending_loan.checkout_date !== null &&
          this.pending_loan.checkout_date !== "" &&
          this.pending_loan.due_date !== null &&
          this.pending_loan.due_date !== "") ||
        (this.pending_loan.checkout_date !== null &&
          this.pending_loan.checkout_date !== "" &&
          this.pending_loan.return_date !== null &&
          this.pending_loan.return_date !== "")
      );
    },
  },
  watch: {},
  methods: {
    ...mapMutations({
      removeMaterial: "loans/removeMaterial",
    }),
    searchUser(query) {
      this.$store.dispatch("users/fetchList", {
        params: { params: { search: query } },
      });
    },
    initInstances(item) {
      return this.$store
        .dispatch("specificmaterials/instances/fetchList", {
          prefix: "specificmaterials/" + item + "/",
        })
        .then((data) => {
          Vue.set(this.specificinstances, item, data);
        });
    },
    submitLoan(e) {
      e.preventDefault();
      this.checkErrors();
      if (this.errors.length) {
        window.scrollTo(0, 0);
      }
      if (!this.emptyLoan && !this.errors.length && !this.emptyInstances) {
        if (this.pending_loan.return_date == "")
          this.pending_loan.return_date = null;

        if (this.updateMode) {
          this.$store
            .dispatch("loans/update", {
              data: this.pending_loan,
              id: this.pending_loan.id,
            })
            .then((data) => {
              this.$store.commit("loans/setPending", data);
              showMsgOk("Le prêt a été modifié");
              this.errors = [];
            })
            .catch((e) => {
              if ("non_field_errors" in e.response.data) {
                this.errors = e.response.data.non_field_errors;
                window.scrollTo(0, 0);
              }
              // eslint-disable-next-line
                console.log(e.response);
            });
        } else {
          if (this.pending_loan.user == null) {
            this.pending_loan.user = this.authUser.id;
          }
          if (this.pending_loan.status == null) {
            this.pending_loan.status = 2;
          }
          this.$store
            .dispatch("loans/create", { data: this.pending_loan })
            .then((data) => {
              this.$store.commit("loans/setPending", data);
              showMsgOk(this.loanMessageSent);
              this.errors = [];
            })
            .catch((e) => {
              if ("non_field_errors" in e.response.data) {
                this.errors = e.response.data.non_field_errors;
                window.scrollTo(0, 0);
              }
              this.errors = [];
              this.errors.push(
                e.response.data.non_field_errors
                  ? e.response.data.non_field_errors[0]
                  : e.response.data
              );
              console.log(this.errors);
              window.scrollTo(0, 0);
              // eslint-disable-next-line
              console.log(e.response);
            });
        }
      }
    },
    checkErrors() {
      this.errors = [];
      if (!this.pending_loan.user && this.canManage) {
        this.errors.push("Un utilisateur doit être assigné");
      }
      if (this.pending_loan.checkout_date > this.pending_loan.due_date) {
        this.errors.push(
          "la date de sortie doit être antérieure à celle du retour prévu"
        );
      }
      if (
        this.pending_loan.return_date &&
        this.pending_loan.checkout_date > this.pending_loan.return_date
      ) {
        this.errors.push(
          "la date de sortie doit être antérieure à celle du retour"
        );
      }
      if (this.emptyInstances) {
        this.errors.push(
          "Veuillez sélectionner une instance pour le matériel spécifique"
        );
      }
    },
    cleanMaterials() {
      this.$store.commit("loans/resetPending");
      this.$store.commit("loans/cleanMaterials");
    },
    newLoan() {
      this.$store.commit("loans/resetPending");
      this.$router.push({ name: "loan" });
    },
    cancelLoan() {
      this.$store
        .dispatch("loans/destroy", { id: this.pending_loan.id })
        .then(() => {
          this.goTo(this.pending_loan.id);
        });
    },
    destroyLoan() {
      this.$store
        .dispatch("loans/destroy", { id: this.pending_loan.id })
        .then(() => {
          this.newLoan();
        });
    },
    makeUserLabel(item) {
      return (
        "@" +
        item.username +
        " (" +
        item.first_name +
        " " +
        item.last_name +
        ")"
      );
    },
    makeLabelInstance(item) {
      return item.name + (item.active ? "" : " (inactif)");
    },
    goTo(id, load = true) {
      if (load) this.$router.push({ name: "loan", params: { loanid: id } });
      this.$store
        .dispatch("loans/fetchSingle", { id: id })
        .then((data) => {
          this.$store
            .dispatch("materials/fetchMaterialsByLoans", { loanids: [data.id] })
            .then(() => {
              this.$store.commit("loans/setPending", data);
            });
          this.$store.dispatch("users/fetchList", {
            params: { params: { userid: data.user } },
          });
        })
        .catch(() => {
          this.newLoan();
        });
    },
    makeChild() {
      this.$store
        .dispatch("loans/makeChild", { id: this.pending_loan.id })
        .then((data) => {
          this.goTo(data.id);
        });
    },
  },
  beforeMount() {
    var pall = [];
    if (this.isAdmin) pall.push(this.$store.dispatch("users/fetchList"));
    pall.push(this.$store.dispatch("entities/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));
    let id = null;
    if (this.loanid) {
      id = parseInt(this.loanid);
    }
    if (id) {
      this.goTo(id, false);
    } else {
      pall.push(
        this.$store.dispatch("materials/fetchMaterialsByIds", {
          gmids: this.pending_loan.generic_materials.map((m) => m.material),
          smids: this.pending_loan.models,
        })
      );
      if (this.canManage) {
        pall.push(
          this.$store.dispatch("users/fetchList", {
            params: { params: { userid: this.pending_loan.user } },
          })
        );
      }
    }
    Promise.all(pall).then(() => {
      //début chargement
      this.loaded = true;
    });
  },
};
</script>
