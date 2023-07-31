<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-auto">
              <h3 v-if="isAuthLoans">Mes prêts</h3>
              <h3 v-if="isEntityLoans">{{ currentEntity.name }}: Prêts</h3>
              <h3 v-if="isMaterialLoans">
                {{ currentEntity.name }}: [{{ materialName }}] Prêts
              </h3>
            </div>
            <div class="col-auto">
              <router-link
                v-if="!isAuthLoans"
                class="btn btn-outline-secondary"
                role="button"
                :to="returnRoute"
              >
                Retour
              </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <input
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              />
            </div>
            <div class="col-auto">
              <div class="input-group">
                <label class="input-group-text" for="statusselect"
                  >Status</label
                >
                <select v-model="statusInput" class="form-control">
                  <option value="">Tous</option>
                  <option
                    v-for="(value, key) in loanStatus"
                    :key="key"
                    :value="key"
                  >
                    {{ value }}
                  </option>
                </select>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check">
                <input
                  id="inProgressInput"
                  v-model="inProgressInput"
                  class="form-check-input"
                  type="checkbox"
                  true-value="null"
                  false-value=""
                />
                <label class="form-check-label" for="inProgressInput">
                  Non rendus
                </label>
              </div>
            </div>
            <div class="col-auto">
              <div class="input-group">
                <label class="input-group-text" for="typeselect"
                  >Ordre :
                </label>
                <select v-model="dateOrderInput" class="form-select">
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
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead>
                <tr>
                  <th>Materiels</th>
                  <th v-if="isAuthLoans">Entité</th>
                  <th v-if="!isAuthLoans">Utilisateur</th>
                  <th>Affiliation</th>
                  <th>Status</th>
                  <th>Date sortie</th>
                  <th>Date retour prévue</th>
                  <th>Date retour</th>
                  <th></th>
                </tr>
              </thead>
              <tbody v-if="loaded">
                <tr v-for="item in loans" :key="item.id">
                  <td>
                    <ul class="list-group list-group-flush">
                      <li
                        v-for="mat in mats[item.id]"
                        :key="mat.material"
                        class="list-group-item border-0 py-0 d-flex justify-content-between align-items-start"
                      >
                        {{
                          mat.quantity
                            ? genericmaterials[mat.material].name
                            : specificmaterials[mat.material].name
                        }}
                        <span
                          v-if="mat.quantity"
                          class="badge rounded-pill"
                          >{{ mat.quantity }}</span
                        >
                      </li>
                    </ul>
                  </td>
                  <td v-if="isAuthLoans">{{ entities[item.entity].name }}</td>
                  <td v-if="!isAuthLoans">
                    <a :href="'mailto:' + users[item.user].email">
                      {{ users[item.user].username }}</a
                    >
                  </td>
                  <td>
                    {{
                      item.affiliation
                        ? affiliations[item.affiliation].name
                        : ""
                    }}
                  </td>
                  <td v-text="loanStatus[item.status]" />
                  <td v-text="item.checkout_date" />
                  <td>{{ item.due_date }}</td>
                  <td v-text="item.return_date" />
                  <td>
                    <button
                      class="btn btn-primary float-end"
                      role="button"
                      @click="toLoan(item.id)"
                    >
                      {{
                        isAuthLoans && item.status != 2
                          ? "Consulter"
                          : "Modifier"
                      }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            v-if="loaded"
            :total="totalCount"
            :per-page="perPage"
            :current-page="currentPage"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import useLoanRouting from "@/composables/useLoanRouting";
import useDebouncedRef from "@/composables/useDebouncedRef";

import { useLoansStore } from "@/stores/loans";
import { useAuthStore } from "@/stores/auth";
import { useAffiliationsStore } from "@/stores/affiliations";
import { useEntitiesStore } from "@/stores/entities";
import { useUsersStore } from "@/stores/users";
import {
  useMaterialsStore,
  useSpecificMaterialsStore,
  useGenericMaterialsStore,
} from "@/stores/materials";
import Pagination from "@/components/nav/ListPagination.vue";
import useSearchStorage from "@/composables/useSearchStorage";

const route = useRoute();

const isAuthLoans = computed(() => route.name == "authloans");
const isEntityLoans = computed(() => route.name == "entityloans");
const isMaterialLoans = computed(
  () =>
    route.name == "specificmaterialloans" ||
    route.name == "genericmaterialloans"
);

const store = useLoansStore();

const { toLoan } = useLoanRouting(store);

const authStore = useAuthStore();
const { authUser } = storeToRefs(authStore);

const affiliationsStore = useAffiliationsStore();
const { objects: affiliations } = storeToRefs(affiliationsStore);
const entitiesStore = useEntitiesStore();
const { objects: entities, currentEntity } = storeToRefs(entitiesStore);
const materialsStore = useMaterialsStore();
const { specificmaterials, genericmaterials } = storeToRefs(materialsStore);
const usersStore = useUsersStore();
const { objects: users } = storeToRefs(usersStore);

const loaded = ref(false);
const returnRoute = computed(() => {
  if (isEntityLoans.value) return { name: "entityinfos" };
  else if (isMaterialLoans.value) return { name: "materialslist" };
  else return "/";
});

const loans = ref([]);
const { count: totalCount, status: loanStatus } = storeToRefs(store);

const mats = ref({});

const sortChoices = {
  due_date: { value: "due_date", label: "Date retour prévue" },
  checkout_date: { value: "-checkout_date", label: "Date sortie" },
  return_date: { value: "return_date", label: "Date de retour" },
};

const searchInput = useDebouncedRef("");
const statusInput = ref();
const dateOrderInput = ref("due_date");
const inProgressInput = ref();
const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

async function fetch(params) {
  loaded.value = false;
  if (isAuthLoans.value)
    loans.value = await store.fetchList({ ...params, user: authUser.value.id });
  else if (isEntityLoans.value)
    loans.value = await store.fetchList({
      ...params,
      entity: currentEntity.value.id,
    });
  else if (isMaterialLoans.value) {
    if (route.name == "genericmaterialloans")
      loans.value = await store.fetchList({
        ...params,
        gm: route.params.matid,
      });
    else if (route.name == "specificmaterialloans")
      loans.value = await store.fetchList({
        ...params,
        sm: route.params.matid,
      });
  }
  if (loans.value.length > 0) {
    let usersIds = new Set();
    let entitiesIds = new Set();
    let affiliationsIds = new Set();
    let genIds = new Set();
    let speIds = new Set();
    let proms = [];
    loans.value.forEach((l) => {
      let matsL = [];
      usersIds.add(l.user);
      entitiesIds.add(l.entity);
      if (l.affiliation) {
        affiliationsIds.add(l.affiliation);
      }
      if (l.generic_materials.length) {
        l.generic_materials.slice(0, 3).forEach((m) => {
          genIds.add(m.material);
          matsL.push(m);
        });
      }
      if (
        l.generic_materials.length < 3 &&
        Object.keys(l.specific_materials).length > 0
      ) {
        Object.keys(l.specific_materials)
          .slice(0, 3 - l.generic_materials.length)
          .forEach((m) => {
            speIds.add(m);
            matsL.push({ material: m });
          });
      }
      mats.value[l.id] = matsL;
    });
    if (isAuthLoans.value)
      proms.push(entitiesStore.fetchList({ ids: [...entitiesIds].join(",") }));
    else {
      proms.push(usersStore.fetchList({ ids: [...usersIds].join(",") }));
    }
    proms.push(
      affiliationsStore.fetchList({ ids: [...affiliationsIds].join(",") })
    );

    proms.push(materialsStore.fetchMaterialsByIds([...genIds], [...speIds]));

    await Promise.all(proms);
    loaded.value = true;
  }
}

const materialName = ref("");

const { refresh } = useSearchStorage(
  route.name,
  fetch,
  {
    search: searchInput,
    status: statusInput,
    rds: inProgressInput,
    ordering: dateOrderInput,
  },
  currentPage,
  perPage.value
);

onBeforeMount(async () => {
  await store.fetchStatus();
  await refresh();
  if (isMaterialLoans.value) {
    if (route.name == "genericmaterialloans")
      materialName.value = (
        await useGenericMaterialsStore().fetchSingle(
          route.params.matid,
          "entities/" + route.params.entityid+ "/"
        )
      ).name;
    else if (route.name == "specificmaterialloans")
      materialName.value = (
        await useSpecificMaterialsStore().fetchSingle(
          route.params.matid,
          "entities/" + route.params.entityid + "/"
        )
      ).name;
  }
  loaded.value = true;
});
</script>
