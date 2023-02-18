<template>
  <div v-if="loaded" class="card">
    <div class="card-header">
      <div class="row justify-content-between">
        <div class="col-auto">
          <h3>{{ currentEntity.name }}: Gestion Matériels</h3>
        </div>
        <div class="col-auto btn-group" role="group">
          <button
            class="btn btn-outline-primary"
            @click.prevent="showHelp = true"
          >
            <span class="badge rounded-pill text-bg-primary">i</span>
          </button>
          <Dropdown
            :items="newMaterialRoutes"
            label="Ajouter un matériel"
            btn-style="btn-outline-primary"
          />
          <router-link
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
      <div class="row  align-items-center">
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
            <label class="input-group-text" for="typeselect">Type</label>
            <select v-model="typeInput" class="form-control">
              <option value="">Les deux</option>
              <option value="g">Generique</option>
              <option value="s">Specifique</option>
            </select>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check">
            <input
              id="hiddenInput"
              v-model="hiddenInput"
              class="form-check-input"
              type="checkbox"
            />
            <label class="form-check-label" for="hiddenInput">
              Afficher matériel caché
            </label>
          </div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Ref Interne</th>
              <th>Ref Fabriquant</th>
              <th>Localisation</th>
              <th>Quantité</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in objectsList"
              :key="item.id + item.name"
              :class="{
                'table-danger': !item.active,
              }"
            >
              <td v-text="item.name" />
              <td>
                {{ item.quantity != undefined ? "Générique" : "Spécifique" }}
              </td>
              <td v-text="item.ref_int" />
              <td v-text="item.ref_man" />
              <td v-text="item.localisation" />
              <td> {{item.quantity != undefined ? item.quantity : item.instances.length }}</td>
              <td class="text-end">
                <router-link
                  class="btn btn-primary m-2"
                  role="button"
                  :to="{ name: (item.quantity!=undefined) ? 'genericmaterial': 'specificmaterial' , params: { matid: item.id } }"
                >
                  Modifier
                </router-link>
                <router-link
                  class="btn btn-primary"
                  role="button"
                  :to="{ name: (item.quantity!=undefined) ? 'genericmaterialloans': 'specificmaterialloans', params: { matid: item.id } }"
                >
                  Voir les prêts
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <pagination
        :total="totalCount"
        :per-page="perPage"
        :current-page="currentPage"
        @pagechanged="onPageChange"
      />
      <modal
        id="modal-help"
        title="Type de matériel"
        :show="showHelp"
        :resolve="
          () => {
            showHelp = false;
          }
        "
      >
        <p>
          Ce site utilise deux type de matériel
          <strong>Spécifique et Générique</strong>
        </p>
        <ul>
          <li>
            Le matériel <strong>Spécifique</strong> correspond au matériel dont
            on ne peut pas intervertir les instances. Par exemple le fablab
            possède 10 tablettes MarqueX (10 instances), chaque tablette a un
            numéro de série, s'il prête la tablette 1 (l'instance 1), il est
            important que ce soit la tablette 1 qui revienne.
          </li>
          <li>
            Le matériel <strong>Générique</strong> correspond au matériel dont
            on peut intervertir les instances. Par exemple, le fablab possède
            des cartes Arduino Uno, quand il prête une carte Arduino Uno, il
            souhaite qu'une carte Arduino Uno soit retournée, mais ce n'est pas
            très grave si ce n'est pas la même que celle prêtée.
          </li>
        </ul>
      </modal>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/composables/useDebouncedRef";

import { useEntitiesStore } from "@/stores/entities";
import { useMaterialsStore } from "@/stores/materials";

import useSearchStorage from "@/composables/useSearchStorage";
import Dropdown from "@/components/ui/Dropdown.vue";
import Pagination from "@/components/nav/ListPagination.vue";
import Modal from "@/plugins/modal";

const entitiesStore = useEntitiesStore();
const { currentEntity } = storeToRefs(entitiesStore);
const route = useRoute();

const store = useMaterialsStore();
const { list: objectsList, count: totalCount } = storeToRefs(store);

const searchInput = useDebouncedRef("");
const typeInput = ref("");
const hiddenInput = ref(true);
const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

async function fetch(params) {
  await store.fetchMaterials(
    { ...params },
    "entities/" + route.params.entityid + "/"
  );
}

const { refresh } = useSearchStorage(
  "materials",
  fetch,
  { search: searchInput, type: typeInput, hidden: hiddenInput },
  currentPage,
  perPage.value
);

const loaded = ref(false);
const newMaterialRoutes = [
  
  {
    to: { name: "genericmaterial", params: { matid: "new" } },
    label: "Générique",
  },
  {
    to: { name: "specificmaterial", params: { matid: "new" } },
    label: "Spécifique",
  },
  /*{
    to: { name: "genericmaterialbulk" },
    label: "Générique massif",
    },*/
];

const returnRoute = computed(() => {
  return { name: "entityinfos", params: route.params };
});

const showHelp = ref(false);

onBeforeMount(async () => {
  await refresh();
  loaded.value = true;
});
</script>
