<template>
  <div>
    <h2 v-if="!matid">
      {{ entityName }}
    </h2>
    <div
      v-if="loaded"
      class="row"
    >
      <div class="col-12 col-md-6">
        <div class="card">
          <div class="card-header">
            <div class="row justify-content-start  align-items-center">
              <div class="col-auto">
                <input
                  v-model="searchInput"
                  class="form-control"
                  type="search"
                  placeholder="Search"
                >
              </div>
              <div class="col-auto">
                <div class="input-group">
                  <label
                    class="input-group-text"
                    for="typeselect"
                  >Ordre :
                  </label>
                  <select
                    v-model="sortInput"
                    class="form-select"
                  >
                    <option
                      v-for="item in sortChoices"
                      :key="item.value"
                      :value="item.value"
                    >
                      {{ item.label }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-check">
                  <label
                    class="form-check-label"
                    for="checkInProgress"
                  >En cours</label>
                  <input
                    id="checkInProgress"
                    v-model="inProgress"
                    type="checkbox"
                    class="form-check-input"
                    aria-label="Checkbox pour prêt en cours"
                  >
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Utilisateur</th>
                    <th>Affiliation</th>
                    <th>Status</th>
                    <th>Date sortie</th>
                    <th>Date retour prévue</th>
                    <th>Date retour</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in objectsList"
                    :key="item.id"
                    :class="{
                      'table-active':
                        selectedObject && item.id == selectedObject.id,
                    }"
                    @click="selectedObject = item"
                  >
                    <td>
                      {{ $filters.field(userById(item.user), "username") }}
                    </td>
                    <td>
                      {{
                        $filters.field(
                          affiliationById(item.affiliation),
                          "name"
                        )
                      }}
                    </td>
                    <td v-text="loanStatus[item.status]" />
                    <td v-text="item.checkout_date" />
                    <td v-text="item.due_date" />
                    <td v-text="item.return_date" />
                  </tr>
                </tbody>
              </table>
            </div>
            <pagination
              :total-pages="pagesCount"
              :total="objectsCount"
              :per-page="perPage"
              :current-page="currentPage"
              @pagechanged="onPageChange"
            />
          </div>
        </div>
      </div>
      <div class="col-12 col-md-6">
        <div
          v-if="selectedObject"
          class="card"
        >
          <div class="card-header">
            <h3
              class="float-start"
              v-text="selectedObject.name"
            />
            <button
              class="btn btn-primary"
              role="button"
              @click="setCopy()"
            >
              Copier
            </button>
            <div
              class="btn-group float-end"
              role="group"
            >
              <button
                class="btn btn-primary"
                role="button"
                @click="editLoan(selectedObject)"
              >
                Modifier
              </button>
              <button
                class="btn btn-danger"
                role="button"
                @click="destroyLoan(selectedObject)"
              >
                Supprimer
              </button>
            </div>
          </div>
          <div class="card-body">
            <table class="table">
              <tr>
                <th scope="row">
                  Utilisateur
                </th>
                <td>
                  <a
                    href=""
                    @click.prevent="showUser()"
                  >
                    {{
                      $filters.field(userById(selectedObject.user), "username")
                    }}</a>
                </td>
              </tr>
              <tr>
                <th scope="row">
                  Affiliation
                </th>
                <td>
                  {{
                    $filters.field(
                      affiliationById(selectedObject.affiliation),
                      "name"
                    )
                  }}
                </td>
              </tr>

              <tr>
                <th scope="row">
                  Status
                </th>
                <td>{{ loanStatus[selectedObject.status] }}</td>
              </tr>
              <tr>
                <th scope="row">
                  Date sortie
                </th>
                <td>{{ selectedObject.checkout_date }}</td>
              </tr>
              <tr>
                <th scope="row">
                  Date retour prévue
                </th>
                <td>{{ selectedObject.due_date }}</td>
              </tr>
              <tr>
                <th scope="row">
                  Date retour
                </th>
                <td>{{ selectedObject.return_date }}</td>
              </tr>
            </table>

            <h5>Commentaires</h5>
            <p class="card-text">
              {{ selectedObject.comments }}
            </p>

            <h5>Matériels</h5>
            <ul
              v-if="!materialsLoading"
              class="list-group"
            >
              <li
                v-for="item in specificMaterials"
                :key="'s' + item.model.id"
                class="list-group-item d-flex justify-content-between align-items-start"
              >
                <div class="ms-2 me-auto">
                  <div class="">
                    {{ item.model.name }}
                  </div>
                  <ul class="list-group">
                    <li
                      v-for="instance in item.instances"
                      :key="instance.id"
                      class="list-group-item"
                    >
                      {{ instance.name }}
                    </li>
                  </ul>
                </div>
              </li>
              <li
                v-for="item in genericMaterials"
                :key="'g' + item.material.id"
                class="list-group-item d-flex justify-content-between align-items-start"
              >
                {{ item.material.name }}
                <span class="badge rounded-pill">{{
                  item.quantity
                }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <modal
      id="modal-user"
      :show="isShowUser"
      title="Utilisateur"
      :resolve="() => (isShowUser = false)"
    >
      <p class="card-text">
        <span><strong>{{ currentUser.username }} :&nbsp;</strong></span>{{ currentUser.first_name }} {{ currentUser.last_name }}
      </p>
      <p>
        <span><strong>Email :&nbsp;</strong></span><a :href="'mailto:' + currentUser.email">{{ currentUser.email }}</a>
      </p>
      <h5>Affiliations</h5>
      <DisplayIdList :items="userAffiliations" />
    </modal>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, inject } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

import ApiService from "@/common/api.service";
import Pagination from "@/components/nav/ListPagination.vue";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Modal from "@/plugins/modal";

import useListFSP from "@/composables/useListFSP";

const store = useStore();
const loaded = ref(true);

const route = useRoute();

const matid = computed(() => route.params.matid);
const entityName = computed(() => {
  let entity = store.getters["entities/byId"](route.params.entityid);
  if (entity) {
    return entity.name;
  } else return "";
});

const fetchParams = ref({});

if (route.name == "loansmaterialgeneric")
  fetchParams.value.gm = route.params.matid;
else if (route.name == "loansmaterialspecific")
  fetchParams.value.sm = route.params.matid;

fetchParams.value.entity = route.params.entityid;

const inProgress = ref(true);
fetchParams.value.rds = "null";

const sortChoices = {
  due_date: { value: "due_date", label: "Date retour prévue" },
  checkout_date: { value: "checkout_date", label: "Date sortie" },
  return_date: { value: "return_date", label: "Date de retour" },
};

const sortInput = ref("due_date");
fetchParams.value.ordering = sortInput.value;

async function postFetch(loans) {
  if (loans.length > 0) {
    const affiliationsIds = new Set(loans.map((l) => l.affiliation));
    const affpromise = store.dispatch("affiliations/fetchList", {
      params: {
        ids: [...affiliationsIds]
          .filter((a) => typeof a === "number")
          .join(","),
      },
    });
    const usersIds = new Set(loans.map((l) => l.user));
    const userpromise = store.dispatch("users/fetchList", {
      params: { ids: [...usersIds].join(",") },
    });
    await affpromise;
    await userpromise;
  }
  return loans;
}

const {
  selectedObject,
  searchInput,
  currentPage,
  pagesCount,
  perPage,
  onPageChange,
  objectsList,
  objectsCount,
  fetchList,
} = useListFSP("loans", { fetchParams, postFetch });

watch(inProgress, () => {
  if (inProgress.value) fetchParams.value.rds = "null";
  else delete fetchParams.value.rds;
  currentPage.value = 1;
  selectedObject.value = null;
  fetchList();
});
watch(sortInput, () => {
  fetchParams.value.ordering = sortInput.value;
  currentPage.value = 1;
  selectedObject.value = null;
  fetchList();
});

const loanStatus = computed(() => store.state.loans.status);
const affiliationById = computed(() => store.getters["affiliations/byId"]);
const userById = computed(() => store.getters["users/byId"]);

const isShowUser = ref(false);
const currentUser = computed(() => userById.value(selectedObject.value.user));
const userAffiliations = ref([]);

async function showUser() {
  isShowUser.value = true;
  const { data } = await ApiService.query("affiliations", {
    ids: currentUser.value.affiliations.join(),
  });
  userAffiliations.value = data.results;
}

const materialsLoading = ref(true);
const genericMaterials = ref([]);
const specificMaterials = ref([]);

watch(selectedObject, async () => {
  if (selectedObject.value) {
    materialsLoading.value = true;
    await store.dispatch("materials/fetchMaterialsByLoan", {
      loanid: selectedObject.value.id,
    });
    genericMaterials.value = selectedObject.value.generic_materials.map(
      (item) => {
        return {
          quantity: item.quantity,
          material: store.getters["materials/genericmaterials"][item.material],
        };
      }
    );
    specificMaterials.value = Object.entries(
      selectedObject.value.specific_materials
    ).map(([model, instances]) => {
      return {
        model: store.getters["materials/specificmaterials"][model],
        instances: store.getters["materials/specificmaterials"][
          model
        ].instances.filter((ins) => instances.includes(ins.id)),
      };
    });
    materialsLoading.value = false;
  } else {
    store.commit("materials/clearMaterials");
    genericMaterials.value = [];
    specificMaterials.value = [];
  }
});

const router = useRouter();
const confirmModal = inject("confirm");

async function setCopy() {
  await store.commit("loans/copyPending", selectedObject.value);
  router.push({ name: "loan" });
}
function editLoan(loan) {
  router.push({ name: "loan", params: { loanid: loan.id } });
}
async function destroyLoan(item) {
  const isConfirmed = await confirmModal({
    content: "Voulez vous vraiment supprimer ce prêt ?",
  });
  if (isConfirmed) {
    await store.dispatch("loans/destroy", {
      id: item.id,
    });
    selectedObject.value=null;
  }
}

onBeforeMount(() => {
  var pall = [];
  pall.push(store.dispatch("loans/fetchStatus"));
  pall.push(fetchList());
  Promise.all(pall).then(() => {
    loaded.value = true;
  });
});
</script>
