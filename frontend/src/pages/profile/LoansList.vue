<template>
  <div class="row">
    <h1 class="col-12">Mes prêts</h1>
    <div class="col-12 col-md-6">
      <div class="card" v-if="loaded">
        <div class="card-header">
          <div class="row gx-2">
            <div class="col-auto">
              <div class="form-check">
                <label class="form-check-label" for="checkInProgress">En cours</label>
                <input
                  id="checkInProgress"
                  v-model="inProgress"
                  type="checkbox"
                  class="form-check-input"
                  aria-label="Checkbox pour prêt en cours"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
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
                  v-for="item in objectsList"
                  :key="item.id"
                  :class="{
                    'table-active':
                      selectedObject && item.id == selectedObject.id,
                  }"
                  @click="selectedObject = item"
                >
                  <td>{{ $filters.field(entityById(item.entity), "name") }}</td>
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
      <div v-if="selectedObject" class="card">
        <div class="card-header">
          <h3 class="float-start" v-text="selectedObject.name" />
          <div class="btn-group float-end" role="group">
            <button
              class="btn btn-primary"
              role="button"
              @click="editLoan(selectedObject)"
            >
              {{ isEditable ? "Modifier" : "Consulter" }}
            </button>
          </div>
        </div>
        <div class="card-body">
          <table class="table">
            <tr>
              <th scope="row">Entité</th>
              <td>
                {{ $filters.field(entityById(selectedObject.entity), "name") }}
              </td>
            </tr>
            <tr>
              <th scope="row">Affiliation</th>
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
              <th scope="row">Status</th>
              <td>{{ loanStatus[selectedObject.status] }}</td>
            </tr>
            <tr>
              <th scope="row">Date sortie</th>
              <td>{{ selectedObject.checkout_date }}</td>
            </tr>
            <tr>
              <th scope="row">Date retour prévue</th>
              <td>{{ selectedObject.due_date }}</td>
            </tr>
            <tr>
              <th scope="row">Date retour</th>
              <td>{{ selectedObject.return_date }}</td>
            </tr>
          </table>

          <h5>Commentaires</h5>
          <p class="card-text">
            {{ selectedObject.comments }}
          </p>

          <h5>Matériels</h5>
          <ul class="list-group" v-if="!materialsLoading">
            <li
              v-for="item in specificMaterials"
              :key="'s' + item.model.id"
              class="list-group-item d-flex justify-content-between align-items-start"
            >
              <div class="ms-2 me-auto">
                <div class="">{{ item.model.name }}</div>
                <ul class="list-group">
                  <li
                    v-for="instance in item.instances"
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
              <span class="badge bg-primary rounded-pill">{{
                item.quantity
              }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onBeforeMount, reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import Pagination from "@/components/nav/ListPagination.vue";

import useListFSP from "@/composables/useListFSP";

const store = useStore();
const loaded = ref(true);

const authUser = computed(() => store.getters.authUser);

const fetchParams = ref({ user: authUser.value.id });

const inProgress = ref(true);
fetchParams.value.rds = "null";

function postFetch(loans) {
  if (loans.length > 0) {
    const entitiesIds = new Set(loans.map((l) => l.entity));
    const affiliationsIds = new Set(loans.map((l) => l.affiliation));
    store.dispatch("entities/fetchList", {
      params: { ids: [...entitiesIds].join(",") },
    });
    store.dispatch("affiliations/fetchList", {
      params: { ids: [...affiliationsIds].join(",") },
    });
  }
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

const loanStatus = computed(() => store.state.loans.status);
const entityById = computed((id) => store.getters["entities/byId"]);
const affiliationById = computed((id) => store.getters["affiliations/byId"]);

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

const isEditable = computed(() => {
  return selectedObject.value && selectedObject.value.status == 2;
});

const router = useRouter();
function editLoan(item) {
  router.push({ name: "loan", params: { loanid: item.id } });
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
