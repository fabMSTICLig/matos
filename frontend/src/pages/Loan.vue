<template>
  <div v-if="loaded">
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-header">
            <h4 class="float-start">
              {{ title }}
            </h4>
            <div
              class="btn-group float-end"
              role="group"
            >
              <router-link
                v-if="updateMode && canManage"
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'entityloans',
                  params: { entityid: pendingLoan.entity },
                }"
              >
                Retour entité
              </router-link>
              <router-link
                v-if="updateMode && !canManage"
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'authloans',
                }"
              >
                Mes prêts
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <ul
              v-show="errors.length != 0"
              class="text-danger"
            >
              <li
                v-for="error in errors"
                :key="error"
                tabIndex="-1"
                v-text="error"
              />
            </ul>
            <form
              class="form"
              @submit.prevent="submitLoan"
            >
              <div class="row">
                <div class="col-12 col-md-5 col-lg-5">
                  <div
                    v-if="canManage"
                    class="mb-3"
                  >
                    <label
                      class="form-label"
                      for="user"
                    >Utilisateur :</label>
                    <Multiselect
                      id="user"
                      ref="msuser"
                      v-model="pendingLoan.user"
                      placeholder="Selectionner un utilisateur"
                      :filter-results="false"
                      :min-chars="3"
                      :resolve-on-load="false"
                      :delay="1"
                      :searchable="true"
                      :options="findUser"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="entity"
                    >Entité :</label>
                    <input
                      id="entity"
                      type="text"
                      class="form-control"
                      :value="entityName"
                      readonly
                    >
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="affiliation"
                    >Affiliation :</label>
                    <Multiselect
                      id="affiliation"
                      v-model="pendingLoan.affiliation"
                      placeholder="Selectionner une affiliation"
                      :options="affiliations"
                      value-prop="id"
                      label="name"
                    />
                  </div>

                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="status"
                    >Status :</label>
                    <select
                      id="status"
                      v-model="pendingLoan.status"
                      class="form-select"
                      :disabled="!canManage"
                    >
                      <option
                        v-for="(val, key) in status"
                        :key="key"
                        :value="key"
                        v-text="val"
                      />
                    </select>
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="checkoutDate"
                    >Date sortie :</label>
                    <input
                      id="checkoutDate"
                      v-model="pendingLoan.checkout_date"
                      class="form-control"
                      type="date"
                      required
                      :disabled="readOnly"
                    >
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="dueDate"
                    >Date retour prévue:</label>
                    <input
                      id="dueDate"
                      v-model="pendingLoan.due_date"
                      class="form-control"
                      type="date"
                      required
                      :disabled="readOnly"
                    >
                  </div>
                  <div
                    v-if="canManage"
                    class="mb-3"
                  >
                    <label
                      class="form-label"
                      for="returnDate"
                    >Date retour:</label>
                    <input
                      id="returnDate"
                      v-model="pendingLoan.return_date"
                      class="form-control"
                      type="date"
                    >
                  </div>

                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="commentary"
                    >Commentaire :</label>
                    <textarea
                      id="commentary"
                      v-model="pendingLoan.comments"
                      class="form-control"
                      :disabled="readOnly"
                    />
                  </div>
                </div>
                <div class="col-12 col-md-7">
                  <p
                    v-show="emptyLoan"
                    class="text-danger"
                  >
                    Votre prêt doit contenir au moins un matériel. Pour un
                    materiel spécifique veuillez choisir une instance
                  </p>

                  <div class="table-responsive-md">
                    <table class="table">
                      <thead>
                        <tr class="d-flex">
                          <th class="col-8">
                            Matériels
                          </th>
                          <th class="col-3">
                            Quantité
                          </th>
                          <th class="col-1" />
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in pendingLoan.generic_materials"
                          :key="'g' + item.material"
                          class="d-flex"
                        >
                          <td class="col-8 disabled">
                            {{ gms[item.material].name }}
                          </td>
                          <td class="col-3 disabled">
                            <input
                              v-model="item.quantity"
                              type="number"
                              min="1"
                              max="10000"
                              class="number-input form-control form-control"
                              :disabled="readOnly"
                            >
                          </td>

                          <td class="col-1 disabled">
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              style="margin-left: -10px"
                              @click="removeMaterial(gms[item.material])"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                        <tr
                          v-for="[key, value] of Object.entries(
                            pendingLoan.specific_materials
                          )"
                          :key="'s' + key"
                          class="d-flex"
                        >
                          <td
                            class="col-11"
                            colspan="2"
                          >
                            {{ sms[key].name }}
                            <div>
                              <h6>Instances</h6>
                              <DynList
                                :model-value="value"
                                :ressource="sms[key].instances"
                                :readonly="readOnly"
                                @update:model-value="
                                  updateSpecificInstance($event, key)
                                "
                              />
                            </div>
                          </td>

                          <td>
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              style="margin-left: -10px"
                              @click="removeMaterial(sms[key])"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div
                    v-if="
                      updateMode &&
                        (pendingLoan.child ||
                          pendingLoan.parent ||
                          pendingLoan.status == 3)
                    "
                    class="mb-3"
                  >
                    <label class="form-label">Historique :</label>
                    <div class>
                      <div
                        role="group"
                        class="btn-group"
                      >
                        <button
                          v-if="updateMode && pendingLoan.parent"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pendingLoan.parent)"
                        >
                          Précédent
                        </button>
                        <button
                          v-if="
                            updateMode &&
                              canManage &&
                              !pendingLoan.child &&
                              pendingLoan.status == 3
                          "
                          class="btn btn-info"
                          type="button"
                          @click="makeChild"
                        >
                          Créer un successeur
                        </button>

                        <button
                          v-if="updateMode && pendingLoan.child"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pendingLoan.child)"
                        >
                          Suivant
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12">
                <div
                  role="group"
                  class="btn-group"
                >
                  <button
                    v-if="!readOnly"
                    class="btn btn-primary float-start"
                    type="submit"
                  >
                    {{ updateMode ? "Modifier" : labelSubmit }}
                  </button>
                  <button
                    v-if="updateMode && !canManage && !readOnly"
                    class="btn btn-danger float-start"
                    type="button"
                    @click="cancelLoan"
                  >
                    Annuler la demande
                  </button>
                  <button
                    v-if="updateMode && canManage"
                    class="btn btn-danger float-start"
                    type="button"
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
                <div
                  role="group"
                  class="btn-group float-end"
                >
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
<script setup>
import { ref, computed, inject, onBeforeMount, defineProps } from "vue";
import { useStore } from "vuex";
import { useRouter, onBeforeRouteUpdate } from "vue-router";
import Multiselect from "@vueform/multiselect";
import DynList from "@/components/ui/DynList.vue";

const store = useStore();
const router = useRouter();
const showModal = inject("show");

const props = defineProps({
  loanid: {
    type: String,
    required: false,
    default: null,
  },
});

const loaded = ref(false);
const authUser = computed(() => store.getters.authUser);
const isAdmin = computed(() => store.getters.isAdmin);
const pendingLoan = computed(() => {
  return store.getters["loans/pendingLoan"];
});

const errors = ref([]);

const loanMessageSent = computed(() => {
  if (pendingLoan.value.status == 2) return "La demande a été envoyée";
  if (pendingLoan.value.status == 3) return "La demande a été acceptée";
  if (pendingLoan.value.status == 4) return "La demande a été refusée";
  if (pendingLoan.value.status == 1) return "La demande a été annulée";

  return "La demande a été envoyée";
});
const labelSubmit = computed(() => {
  if (canManage.value && !updateMode.value) {
    return "Créer";
  } else {
    return "Envoyer la demande";
  }
});
const emptyLoan = computed(() => {
  return (
    pendingLoan.value.generic_materials.length == 0 &&
    Object.values(pendingLoan.value.specific_materials).reduce(
      (p, v) => p + v.length,
      0
    ) == 0
  );
});
const canManage = computed(() => {
  return (
    isAdmin.value ||
    authUser.value.entities.indexOf(pendingLoan.value.entity) > -1
  );
});
const updateMode = computed(() => {
  return pendingLoan.value && "id" in pendingLoan.value;
});
const readOnly = computed(() => {
  return !canManage.value && pendingLoan.value.status != 2;
});
const title = computed(() => {
  return readOnly.value
    ? "Consulter prêt"
    : updateMode.value
    ? "Modification prêt"
    : "Nouveau prêt";
});

const msuser = ref();
async function findUser(query) {
  let users = await store.dispatch("users/fetchList", {
    params: { search: query },
  });
  return users.map((u) => {
    return {
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    };
  });
}

const entityName = computed(() => {
  if (pendingLoan.value.entity)
    return store.getters["entities/byId"](pendingLoan.value.entity).name;
  else return "";
});

const status = computed(() => store.getters["loans/status"]);

const affiliations = computed(() => store.getters["affiliations/list"]);
const gms = computed(() => {
  return store.getters["materials/genericmaterials"];
});
const sms = computed(() => {
  return store.getters["materials/specificmaterials"];
});

function updateSpecificInstance(instances, model) {
  pendingLoan.value.specific_materials[model] = instances;
  store.commit("loans/savePending");
}

async function loadLoan(id = null) {
  if (id) {
    await store.dispatch("loans/onLoad", id);
    router.push({ name: "loan" });
  }
  await store.dispatch("affiliations/fetchList", { params: { limit: 1000 } });
  await store.dispatch("loans/fetchStatus");
  await store.dispatch("materials/fetchMaterials", {
    params: {
      gmids: pendingLoan.value.generic_materials.map((o) => o.material).join(),
      smids: Object.keys(pendingLoan.value.specific_materials).join(),
    },
  });
  if (pendingLoan.value.entity)
    await store.dispatch("entities/fetchSingle", {
      id: pendingLoan.value.entity,
    });
  loaded.value = true;
  if (pendingLoan.value.user) {
    let u = await store.dispatch("users/fetchSingle", {
      id: pendingLoan.value.user,
    });
    msuser.value.select({
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    });
  }
}

onBeforeMount(async () => {
  await loadLoan(props.loanid);
});

function handleErrors(e) {
  errors.value = [];
  if (e.response)
    errors.value.push(
      e.response.data.non_field_errors
        ? e.response.data.non_field_errors[0]
        : e.response.data
    );
  else console.log(e);
  console.log(errors.value);
  window.scrollTo(0, 0);
  // eslint-disable-next-line
  console.log(e.response);
}

async function submitLoan() {
  checkErrors();
  if (errors.value.length) {
    window.scrollTo(0, 0);
  }
  if (!emptyLoan.value && !errors.value.length) {
    if (pendingLoan.value.return_date == "")
      pendingLoan.value.return_date = null;

    if (updateMode.value) {
      try {
        let data = await store.dispatch("loans/update", {
          data: pendingLoan.value,
          id: pendingLoan.value.id,
        });
        store.commit("loans/setPending", data);
        showModal({ content: "Le prêt a été modifié" });
        errors.value = [];
      } catch (e) {
        handleErrors(e);
      }
    } else {
      if (pendingLoan.value.user == null) {
        pendingLoan.value.user = authUser.value.id;
      }
      if (pendingLoan.value.status == null) {
        pendingLoan.value.status = 2;
      }
      try {
        let data = await store.dispatch("loans/create", {
          data: pendingLoan.value,
        });
        store.commit("loans/setPending", data);
        showModal({ content: loanMessageSent.value });
        errors.value = [];
      } catch (e) {
        handleErrors(e);
      }
    }
  }
}
function checkErrors() {
  errors.value = [];
  if (!pendingLoan.value.user && canManage.value) {
    errors.value.push("Un utilisateur doit être assigné");
  }
  if (pendingLoan.value.checkout_date > pendingLoan.value.due_date) {
    errors.value.push(
      "la date de sortie doit être antérieure à celle du retour prévu"
    );
  }
  if (
    pendingLoan.value.return_date &&
    pendingLoan.value.checkout_date > pendingLoan.value.return_date
  ) {
    errors.value.push(
      "la date de sortie doit être antérieure à celle du retour"
    );
  }
}

function removeMaterial(mat) {
  store.dispatch("loans/removeMaterial", mat);
}
function cleanMaterials() {
  store.commit("loans/resetPending");
}
function newLoan() {
  store.commit("loans/resetPending");
  router.push({ name: "loan" });
}
function cancelLoan() {
  store.dispatch("loans/destroy", { id: pendingLoan.value.id }).then(() => {
    goTo(pendingLoan.value.id);
  });
}
function destroyLoan() {
  store.dispatch("loans/destroy", { id: pendingLoan.value.id }).then(() => {
    newLoan();
  });
}
async function makeChild() {
  try {
    await store
      .dispatch("loans/makeChild", { id: pendingLoan.value.id })
      .then((data) => {
        goTo(data.id);
      });
  } catch (e) {
    handleErrors(e);
  }
}
function goTo(id, load = true) {
  if (load) router.push({ name: "loan", params: { loanid: id } });
}
onBeforeRouteUpdate((to) => {
  loadLoan(to.params["loanid"]);
});
</script>
