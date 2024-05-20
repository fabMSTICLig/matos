<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <div v-if="loaded" class="row">
    <div class="col">
      <div class="card">
        <div class="card-header">
          <h4 class="float-start">
            {{ title }}
          </h4>
          <div class="btn-group float-end" role="group">
            <button
              v-if="!isBasket && canManage"
              class="btn btn-danger"
              type="button"
              @click="destroyLoan"
            >
              Supprimer
            </button>
            <button
              v-if="isBasket"
              class="btn btn-danger"
              type="button"
              @click="resetBasket"
            >
              Vider panier
            </button>
          </div>
        </div>
        <div class="card-body">
          <ul v-show="errors.length != 0" class="text-danger">
            <li
              v-for="error in errors"
              :key="error"
              tabIndex="-1"
              v-text="error"
            />
          </ul>
          <form ref="editorForm" class="form" novalidate>
            <div class="row">
              <div class="col-12 col-md-5 col-lg-5">
                <div v-if="canManage" class="mb-3">
                  <label class="form-label" for="user">Utilisateur :</label>
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
                    @select="userChanged"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="entity">Entité :</label>
                  <input
                    id="entity"
                    type="text"
                    class="form-control"
                    :value="entityName"
                    readonly
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="affiliation"
                    >Affiliation :</label
                  >
                  <Multiselect
                    id="affiliation"
                    v-model="pendingLoan.affiliation"
                    placeholder="Selectionner une affiliation"
                    :options="affiliations"
                    :searchable="true"
                    value-prop="id"
                    label="name"
                    :disabled="readOnly"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="checkoutDate"
                    >Date sortie :</label
                  >
                  <input
                    id="checkoutDate"
                    v-model="pendingLoan.checkout_date"
                    class="form-control"
                    type="date"
                    required
                    :disabled="readOnly"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="dueDate"
                    >Date retour prévue:</label
                  >
                  <input
                    id="dueDate"
                    v-model="pendingLoan.due_date"
                    class="form-control"
                    type="date"
                    required
                    :disabled="readOnly"
                  />
                </div>
                <div
                  v-if="
                    !isBasket &&
                    readOnly &&
                    !pendingLoan.return_date &&
                    pendingLoan.status == 3
                  "
                  class="mb-3"
                >
                  <label class="form-label" for="extDate"
                    >Demande prolongation:</label
                  >
                  <input
                    v-if="!extMsg"
                    id="extDate"
                    v-model="extDate"
                    class="form-control"
                    type="date"
                  />
                  <button
                    v-if="!extMsg"
                    type="button"
                    class="btn btn-warning"
                    @click="askExtension"
                  >
                    Demander
                  </button>
                  <p v-if="extMsg">
                    Vous avez déjà envoyé une demande de prolongation à la date
                    {{ extMsg }}.<br />
                    Si vous avez besoin de modifier la date, merci de contacter
                    l'entité directement par mail.
                  </p>
                </div>

                <div v-if="canManage" class="mb-3">
                  <label class="form-label" for="returnDate"
                    >Date retour:</label
                  >
                  <input
                    id="returnDate"
                    v-model="pendingLoan.return_date"
                    class="form-control"
                    type="date"
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label" for="commentary"
                    >Commentaire :</label
                  >
                  <textarea
                    id="commentary"
                    v-model="pendingLoan.comments"
                    class="form-control"
                    :disabled="readOnly"
                  />
                </div>
                <div v-if="!isBasket" class="mb-3">
                  <p>
                    Status :
                    <small
                      >(Un mail sera envoyé automatiquement pour tout changement
                      de status)</small
                    >
                  </p>
                  <div class="form-check form-check-inline">
                    <input
                      id="inlineRadio1"
                      v-model="pendingLoan.status"
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      value="2"
                      :disabled="!canManage && pendingLoan.status != 2"
                    />
                    <label class="form-check-label" for="inlineRadio1"
                      >En attente</label
                    >
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      id="inlineRadio2"
                      v-model="pendingLoan.status"
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      value="3"
                      :disabled="!canManage && pendingLoan.status != 3"
                    />
                    <label class="form-check-label" for="inlineRadio2"
                      >Accepté</label
                    >
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      id="inlineRadio3"
                      v-model="pendingLoan.status"
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      value="4"
                      :disabled="!canManage && pendingLoan.status != 4"
                    />
                    <label class="form-check-label" for="inlineRadio3"
                      >Refusé</label
                    >
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      id="inlineRadio4"
                      v-model="pendingLoan.status"
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      value="1"
                      :disabled="!canManage && pendingLoan.status != 1"
                    />
                    <label class="form-check-label" for="inlineRadio4"
                      >Annulé</label
                    >
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-7">
                <p v-show="isEmptyLoan" class="text-danger">
                  Votre prêt doit contenir au moins un matériel.
                </p>
                <p v-show="isEmptySpeMat" class="text-danger">
                  Pour chaque materiel spécifique, veuillez choisir au moins une
                  instance. Si vous ne savez pas quelle instance choisir, prenez
                  en une au hasard, le gestionnaire de l'entité la modifira au
                  moment de la validtion.
                </p>
                <div class="table-responsive-md">
                  <table class="table">
                    <thead>
                      <tr class="d-flex">
                        <th class="col-8">Matériels</th>
                        <th class="col-3">Quantité</th>
                        <th class="col-1" />
                      </tr>
                    </thead>
                    <tbody v-if="matsLoaded">
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
                          />
                        </td>

                        <td class="col-1 disabled">
                          <button
                            v-if="!readOnly"
                            class="btn btn-danger"
                            type="button"
                            @click="
                              removeMaterial(gms[item.material], isBasket)
                            "
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
                        <td class="col-11" colspan="2">
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
                            @click="removeMaterial(sms[key], isBasket)"
                          >
                            X
                          </button>
                        </td>
                      </tr>
                      <tr v-if="!readOnly">
                        <td>
                          <router-link
                            :to="{
                              name: isBasket ? 'search' : 'addmaterial',
                            }"
                            class="btn btn-primary float-end"
                            role="button"
                            >Ajouter un matériel</router-link
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div class="col-12">
              <div v-if="!isBasket" class="float-start">
                <strong>Historique: </strong>
                <div role="group" class="btn-group">
                  <button
                    class="btn btn-outline-info"
                    type="button"
                    @click.prevent="showHelp = true"
                  >
                    <span class="badge rounded-pill">i</span>
                  </button>
                  <router-link
                    v-if="pendingLoan.parent"
                    class="btn btn-outline-primary"
                    :to="{
                      name: 'loan',
                      params: { loanid: pendingLoan.parent },
                    }"
                  >
                    Précédent
                  </router-link>
                  <router-link
                    v-if="pendingLoan.child"
                    class="btn btn-outline-primary"
                    :to="{
                      name: 'loan',
                      params: { loanid: pendingLoan.child },
                    }"
                  >
                    Suivant
                  </router-link>
                  <button
                    v-if="historyChange"
                    class="btn btn-info"
                    type="button"
                    @click.prevent="updateLoan(true)"
                  >
                    Modifier avec historique
                  </button>
                </div>
              </div>
              <div v-if="isBasket" role="group" class="btn-group float-end">
                <button
                  class="btn btn-primary"
                  type="button"
                  @click.prevent="sendRequest()"
                >
                  Envoyer la demande
                </button>
              </div>
              <div v-else role="group" class="btn-group float-end">
                <button
                  v-if="isAuthLoan && !canManage && !readOnly"
                  class="btn btn-danger"
                  type="button"
                  @click="cancelLoan()"
                >
                  Annuler la demande
                </button>

                <button
                  v-if="!readOnly || canManage"
                  class="btn btn-primary"
                  type="button"
                  @click.prevent="updateLoan()"
                >
                  Modifier
                </button>
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click.prevent="goBack()"
                >
                  {{ readOnly ? "Retour" : "Annuler" }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <modal
      id="modal-help"
      title="Historique de prêt"
      :show="showHelp"
      :resolve="
        () => {
          showHelp = false;
        }
      "
    >
      <p>
        Exemple d'utilisation: une personne emprunte 3 matériels différents pour
        1 mois, après une semaine elle revient pour rendre 1 matériel sur les 3
        et en prendre 2 nouveaux. Une modification avec historique va cloturer
        le premier prêt à la date d'aujourd'hui mais sans appliquer de
        changement et créer une copie qui débutera aujourd'hui avec les
        changements appliqués. Un lien sera fait entre les deux prêts.
      </p>
      <p>Les conditions pour faire une modification avec historique:</p>
      <ul>
        <li>le prêt doit être accepté et non rendu</li>
        <li>une date de retour prévue dans le future</li>
        <li>l'emprunteur ou la liste de matériel ont changé</li>
      </ul>
    </modal>
  </div>
</template>
<script setup>
import { ref, computed, watch, inject, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import Multiselect from "@vueform/multiselect";
import DynList from "@/components/ui/DynList.vue";

import { useLoansStore } from "@/stores/loans";
import { useAuthStore } from "@/stores/auth";
import { useAffiliationsStore } from "@/stores/affiliations";
import { useEntitiesStore } from "@/stores/entities";
import { useUsersStore } from "@/stores/users";
import { useMaterialsStore } from "@/stores/materials";

import useLoanRouting from "@/composables/useLoanRouting";
import Modal from "@/plugins/modal";

const store = useLoansStore();

const authStore = useAuthStore();
const { authUser, isAdmin } = storeToRefs(authStore);

const { basket, currentLoan, historyChange } = storeToRefs(store);

const { initBasket, cancelCurrent, removeMaterial, resetBasket } = store;

const { isAuthLoan, goBack, initOrigin } = useLoanRouting(store, authUser);

const router = useRouter();
const route = useRoute();
const showModal = inject("show");
const confirmModal = inject("confirm");
const showHelp = ref(false);

const isBasket = computed(() => route.name == "basket");

const pendingLoan = isBasket.value ? ref(basket) : ref(currentLoan);

const canManage = computed(() => {
  return (
    isAdmin.value ||
    authUser.value.entities.indexOf(pendingLoan.value.entity) > -1
  );
});
const isEmptyLoan = computed(() => {
  return pendingLoan.value.generic_materials.length == 0 && isEmptySpeMat.value;
});
const isEmptySpeMat = computed(() => {
  let spemats = Object.values(pendingLoan.value.specific_materials)
  if(spemats.length==0) return 0;
  else return Object.values(pendingLoan.value.specific_materials).some(
    (v) => v.length == 0
  );
});
const readOnly = computed(() => {
  return !canManage.value && pendingLoan.value.status != 2;
});

const props = defineProps({
  loanid: {
    type: String,
    required: false,
    default: null,
  },
});

const loaded = ref(false);
const matsLoaded = ref(false);
const editorForm = ref(null);
const errors = ref([]);

const title = computed(() => {
  if (isBasket.value) return "Panier";
  else if (isAuthLoan.value)
    return pendingLoan.value.status == 2 ? "Modifier prêt" : "Consulter prêt";
  else return entityName.value + ": Modifier prêt";
});

const usersStore = useUsersStore();
const msuser = ref();
async function findUser(query) {
  let users = await usersStore.fetchList({ search: query });
  return users.map((u) => {
    return {
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
      affiliations: u.affiliations,
    };
  });
}

function userChanged(uid) {
  let user = usersStore.objects[uid];
  pendingLoan.value.affiliation =
    user.affiliations.length > 0 ? user.affiliations[0] : null;
}

const entitiesStore = useEntitiesStore();
const { objects: entities } = storeToRefs(entitiesStore);
const entityName = computed(() => {
  if (pendingLoan.value.entity) {
    return entities.value[pendingLoan.value.entity].name;
  } else return "";
});

const affiliationsStore = useAffiliationsStore();
const { list: affiliations } = storeToRefs(affiliationsStore);

const materialsStore = useMaterialsStore();
const { specificmaterials: sms, genericmaterials: gms } =
  storeToRefs(materialsStore);

function updateSpecificInstance(instances, model) {
  pendingLoan.value.specific_materials[model] = instances;
}

//Mounted pour avoir accés à la ref msuser
onMounted(async () => {
  store.fetchStatus();
  await affiliationsStore.fetchList({ limit: 1000 });
  await entitiesStore.fetchList({ limit: 1000 });
  if (isBasket.value) {
    initBasket();
  } else {
    await store.setCurrent(props.loanid);
    initOrigin();
  }
  await loadLoan();
});

watch(props, async () => {
  matsLoaded.value = false;
  await store.setCurrent(props.loanid);
  await loadLoan();
});

async function loadLoan() {
  await materialsStore.fetchMaterials({
    gmids: pendingLoan.value.generic_materials.map((o) => o.material).join(),
    smids: Object.keys(pendingLoan.value.specific_materials).join(),
    hidden: true,
  });
  matsLoaded.value = true;
  loaded.value = true;
  if (pendingLoan.value.user && canManage.value) {
    let u = await usersStore.fetchSingle(pendingLoan.value.user);
    if (canManage.value) {
      msuser.value.select({
        label: "@" + u.username + " " + u.first_name + " " + u.last_name,
        value: u.id,
      });
    }
  }
}

function handleErrors(e) {
  errors.value = [];
  if (e.response)
    errors.value.push(
      e.response.data.non_field_errors
        ? e.response.data.non_field_errors[0]
        : e.response.data
    );
  else console.log(e);
  window.scrollTo(0, 0);
}

async function sendRequest() {
  if (!isEmptyLoan.value && !isEmptySpeMat.value && !checkErrors()) {
    if (pendingLoan.value.return_date == "")
      pendingLoan.value.return_date = null;
    try {
      await store.create(basket.value);
      store.resetBasket();
      router.push({ name: "authloans" });
    } catch (e) {
      handleErrors(e);
      return false;
    }
    return true;
  } else {
    window.scrollTo(0, 0);
  }
}

async function updateLoan(hist = false) {
  if (!isEmptyLoan.value && !isEmptySpeMat.value && !checkErrors()) {
    if (pendingLoan.value.return_date == "")
      pendingLoan.value.return_date = null;
    else if (pendingLoan.value.status == 2) {
      showModal({
        content:
          "Un prêt ne peut être en attente avec une date de retour. Il est possible que vous ayez oublié de l'accepter.",
      });
      return false;
    }
    try {
      await store.updateCurrent(hist);
      goBack();
      //loaded a faux avant de mettre le prêt a null
      // pour eviter ile refresh de la page avant le changement de page
      loaded.value = false;
      store.setCurrent(null);
    } catch (e) {
      handleErrors(e);
      return false;
    }
    return true;
  } else {
    window.scrollTo(0, 0);
    return false;
  }
}

async function cancelLoan() {
  await cancelCurrent();
  goBack();
}

function checkErrors() {
  if (!editorForm.value.checkValidity()) {
    editorForm.value.reportValidity();
    return true;
  }
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
  return errors.value.length != 0;
}

async function destroyLoan() {
  const isConfirmed = await confirmModal({
    content: "Voulez vous vraiment supprimer ce prêt ?",
  });
  if (isConfirmed) store.destroy(pendingLoan.value.id);
}

/////////// ask extenstion
const extLoans = ref(
  JSON.parse(
    sessionStorage.getItem("extLoans")
      ? sessionStorage.getItem("extLoans")
      : "{}"
  )
);
const extMsg = computed(() => {
  if (extLoans.value) {
    if (pendingLoan.value.id in extLoans.value) {
      return extLoans.value[pendingLoan.value.id];
    }
  }
  return "";
});
const extDate = ref();
async function askExtension() {
  const isConfirmed = await confirmModal({
    content:
      "Voulez vous vraiment envoyer une demande de prolongation du prêt ?",
  });
  if (isConfirmed) {
    try {
      await store.askExtension(pendingLoan.value.id, extDate.value);
      showModal({
        content:
          "Demande envoyée. Veuillez attendre la réponse de l'entité avant d'envoyer une nouvelle demande.",
      });
      extLoans.value[pendingLoan.value.id] = extDate.value;
      sessionStorage.setItem("extLoans", JSON.stringify(extLoans.value));
    } catch (e) {
      showModal({ content: e.response.data });
    }
  }
}
</script>
