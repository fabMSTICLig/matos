<template>
  <div v-if="loaded" class="row">
    <div class="col-12 col-md-12 col-lg-6">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between align-items-center">
            <div class="col-6">
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
              <Dropdown
                :items="newMaterialRoutes"
                label="Ajouter"
                classtoogle="btn-primary"
                :button="true"
              />
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objectsList"
                  :key="item.id + item.name"
                  :class="{
                    'table-active':
                      selectedObject &&
                      item.id + item.name ==
                        selectedObject.id + selectedObject.name,
                    'table-danger': !item.active,
                  }"
                  @click="selectedObject = item"
                >
                  <td v-text="item.name" />
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
          <h3 class="float-start">
            Matériel {{ isGeneric ? "Générique" : "Spécifique" }}
          </h3>
          <div class="btn-group float-end" role="group">
            <router-link class="btn btn-primary" role="button" :to="loansRoute">
              Prêts
            </router-link>
            <router-link class="btn btn-primary" role="button" :to="editRoute">
              Modifier
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <h3>
            {{ selectedObject.name }}
          </h3>
          <markdown :description="selectedObject.description" />
          <table class="table">
            <tr>
              <th scope="row">Ref interne</th>
              <td>{{ selectedObject.ref_int }}</td>
            </tr>
            <tr>
              <th scope="row">Ref fabricant</th>
              <td>{{ selectedObject.ref_man }}</td>
            </tr>
            <tr>
              <th scope="row">Localisation</th>
              <td>{{ selectedObject.localisation }}</td>
            </tr>
            <tr v-if="isGeneric">
              <th scope="row">Quantité</th>
              <td>{{ selectedObject.quantity }}</td>
            </tr>
            <tr v-if="!selectedObject.active" class="text-danger">
              <th scope="row">Visibilité</th>
              <td>Invisible</td>
            </tr>
          </table>
          <p v-if="!isGeneric">
            <span><strong>Instances :&nbsp;</strong></span>
            <DisplayIdList :items="selectedInstances" />
          </p>

          <p>
            <span><strong>Tags :&nbsp;</strong></span>
            <DisplayIdList :items="selectedTags" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import useDebouncedRef from "@/composables/useDebouncedRef";

import Dropdown from "@/components/ui/Dropdown.vue";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/Markdown.vue";
import Pagination from "@/components/nav/ListPagination.vue";

const store = useStore();
const route = useRoute();

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
  {
    to: { name: "genericmaterialbulk" },
    label: "Générique massif",
  },
];

const objectsList = computed(() => {
  return store.getters["materials/list"];
});
const objectsCount = computed(() => {
  return store.state["materials"].count;
});

const selectedObject = ref(null);
const selectedTags = computed(() => store.getters["tags/list"]);
const selectedInstances = computed(() =>
  selectedObject.value ? selectedObject.value.instances : []
);
const isGeneric = computed(() => {
  return "quantity" in selectedObject.value;
});

const ssObject = "entitymatlist_object";
const ssSearch = "entitymatlist_search";
const ssType = "entitymatlist_type";

function ssGetOrDefault(key, defaultValue) {
  return sessionStorage.getItem(key)
    ? sessionStorage.getItem(key)
    : defaultValue;
}

watch(selectedObject, () => {
  if (selectedObject.value) {
    sessionStorage.setItem(
      ssObject,
      "" + selectedObject.value.id + selectedObject.value.name
    );
    if (selectedObject.value.tags)
      store.dispatch("tags/fetchList", {
        params: { ids: selectedObject.value.tags.join(",") },
      });
  } else sessionStorage.removeItem(ssObject);
});

const searchInput = useDebouncedRef(ssGetOrDefault(ssSearch, ""));
const typeInput = ref(ssGetOrDefault(ssType, ""));

watch([searchInput, typeInput], () => {
  currentPage.value = 1;
  fetchList();
});
watch([searchInput], () => {
  sessionStorage.setItem(ssSearch, searchInput.value);
});
watch([typeInput], () => {
  sessionStorage.setItem(ssType, typeInput.value);
});

const currentPage = ref(1);

const pagesCount = computed(() => {
  return Math.ceil(objectsCount.value / import.meta.env.VITE_APP_MAXLIST);
});
const perPage = computed(() => {
  return parseInt(import.meta.env.VITE_APP_MAXLIST);
});

function onPageChange(page) {
  currentPage.value = page;
  sessionStorage.setItem("materials_page", page);
  fetchList();
}

function loadPage() {
  if (sessionStorage.getItem("materials_page")) {
    currentPage.value = parseInt(sessionStorage.getItem("materials_page"));
  }
}

const editRoute = computed(() => {
  let name = "specificmaterial";
  if ("quantity" in selectedObject.value) {
    name = "genericmaterial";
  }
  return { name: name, params: { matid: selectedObject.value.id } };
});
const loansRoute = computed(() => {
  var name = "loansmaterialspecific";
  if ("quantity" in selectedObject.value) {
    name = "loansmaterialgeneric";
  }
  return {
    name: name,
    params: {
      matid: selectedObject.value.id,
      entityid: route.params.entityid,
    },
  };
});

function fetchList() {
  let paramsDefault = {};
  if (searchInput.value) {
    paramsDefault["search"] = searchInput.value;
  }
  paramsDefault["type"] = typeInput.value;

  paramsDefault.limit = import.meta.env.VITE_APP_MAXLIST;
  paramsDefault.offset =
    (currentPage.value - 1) * import.meta.env.VITE_APP_MAXLIST;
  return store
    .dispatch("materials/fetchMaterials", {
      prefix: "entities/" + route.params.entityid + "/",
      params: { ...paramsDefault },
    })
    .then((list) => {
      let obj = null;
      if (sessionStorage.getItem("materials_object")) {
        let id = sessionStorage.getItem("materials_object");
        obj = list.find((o) => o.id + o.name == id);
      }
      if (obj) selectedObject.value = obj;
      else selectedObject.value = list[0];
      return list;
    });
}

onBeforeMount(async () => {
  loadPage();
  const list = await fetchList();
  loaded.value = true;

  return list;
});
</script>
