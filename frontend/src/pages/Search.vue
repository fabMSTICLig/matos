<template>
  <div>
    <h1>Rechercher</h1>
    <div
      v-if="loaded"
      class="row"
    >
      <div class="col-xl-3">
        <div class="card">
          <div class="card-header">
            <h4>Filtres</h4>
          </div>
          <div class="card-body">
            <form class="form">
              <div class="mb-3">
                <label
                  class="form-label"
                  for="searchInput"
                >Chercher</label><input
                  id="searchInput"
                  v-model="searchInput"
                  type="search"
                  class="form-control"
                  placeholder="Arduino"
                >
              </div>
              <div class="mb-3">
                <label
                  class="form-label"
                  for="typeInput"
                >Type</label>
                <select
                  id="typeInput"
                  v-model="typeInput"
                  class="form-control"
                >
                  <option value="">
                    Les deux
                  </option>
                  <option value="g">
                    Generique
                  </option>
                  <option value="s">
                    Specifique
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Entités</label>
                <TagsInput
                  v-model="entitiesInput"
                  ressource="entities"
                  forbid-add
                  no-load
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Tags</label>
                <TagsInput
                  v-model="tagsInput"
                  ressource="tags"
                  forbid-add
                  no-load
                />
              </div>
              <div
                v-if="isAdmin || authUser.entities.length"
                class="mb-3 form-check form-switch"
              >
                <input
                  id="check-active"
                  v-model="hiddenInput"
                  type="checkbox"
                  class="form-check-input"
                >
                <label
                  class="form-check-label"
                  for="check-active"
                >Invisible</label>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            <pagination
              :total-pages="pagesCount"
              :total="objectsCount"
              :per-page="perPage"
              :current-page="currentPage"
              @pagechanged="onPageChange"
            />
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="item in objectsList"
                :key="item.name + item.id"
                class="list-group-item list-group-item-action flex-column align-items-start"
              >
                <div class="d-flex w-100 justify-content-between">
                  <a
                    href="#"
                    @click.prevent="goToMaterial(item)"
                  ><h4>{{ item.name }}</h4></a>
                  <strong><router-link
                    :to="{
                      name: 'entityinfos',
                      params: { entityid: item.entity },
                    }"
                  >{{ getEntityName(item.entity) }}</router-link></strong>
                </div>
                <markdown :description="item.description" />
                <p>
                  <strong>Tags :</strong>
                  <DisplayIdList :items="getTags(item.tags)" />
                </p>

                <button
                  class="btn btn-primary wt-1"
                  type="button"
                  :class="{
                    disabled:
                      pendingLoan.entity && pendingLoan.entity != item.entity,
                  }"
                  title="Les matériels d'un prêt doivent tous appartenir à la même entité"
                  @click="addItem(item)"
                >
                  Ajouter
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import useDebouncedRef from "@/composables/useDebouncedRef";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/Markdown.vue";
import TagsInput from "@/components/ui/TagsInput.vue";
import Pagination from "@/components/nav/ListPagination.vue";

const store = useStore();
const router = useRouter();

const loaded = ref(false);
const authUser = computed(() => store.getters.authUser);
const isAdmin = computed(() => store.getters.isAdmin);

const objectsList = computed(() => {
  return store.getters["materials/list"];
});
const objectsCount = computed(() => {
  return store.state["materials"].count;
});

const pendingLoan = computed(() => store.getters["loans/pendingLoan"]);
function getTags(tagids) {
  return tagids.map((id) => store.getters["tags/byId"](id));
}

function goToMaterial(item) {
  if (item.instances) {
    router.push({
      name: "specificmaterialitem",
      params: { matid: item.id },
    });
  } else {
    router.push({
      name: "genericmaterialitem",
      params: { matid: item.id },
    });
  }
}
function addItem(item) {
  if (pendingLoan.value.entity == null && entitiesInput.value.indexOf(item.entity)==-1) {
    entitiesInput.value.push(item.entity);
  }
  store.dispatch("loans/addMaterial", item);
}
function getEntityName(id) {
  let entity = store.getters["entities/byId"](id);
  if (entity) return entity.name;
  else return "";
}

function ssGetOrDefault(key, defaultValue) {
  return sessionStorage.getItem(key)
    ? sessionStorage.getItem(key)
    : defaultValue;
}

const ssSearch = "search_search";
const ssType = "search_type";
const ssEntities = "search_entities";
const ssTags = "search_tags";
const ssHidden = "search_hidden";

const searchInput = useDebouncedRef(ssGetOrDefault(ssSearch, ""));
const typeInput = ref(ssGetOrDefault(ssType, ""));
const entitiesInput = ref(JSON.parse(ssGetOrDefault(ssEntities, "[]")));
const tagsInput = ref(JSON.parse(ssGetOrDefault(ssTags, "[]")));
const hiddenInput = ref(JSON.parse(ssGetOrDefault(ssHidden, "false")));

watch([searchInput, typeInput, entitiesInput, tagsInput, hiddenInput], () => {
  currentPage.value = 1;
  fetchList();
});
watch(searchInput, () => {
  sessionStorage.setItem(ssSearch, searchInput.value);
});
watch(typeInput, () => {
  sessionStorage.setItem(ssType, typeInput.value);
});
watch(entitiesInput, () => {
  sessionStorage.setItem(ssEntities, JSON.stringify(entitiesInput.value));
});
watch(tagsInput, () => {
  sessionStorage.setItem(ssTags, JSON.stringify(tagsInput.value));
});
watch(hiddenInput, () => {
  sessionStorage.setItem(ssHidden, JSON.stringify(hiddenInput.value));
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
  sessionStorage.setItem("search_page", page);
  fetchList();
}

function loadPage() {
  if (sessionStorage.getItem("search_page")) {
    currentPage.value = parseInt(sessionStorage.getItem("search_page"));
  }
}

function fetchList() {
  let paramsDefault = {};
  if (searchInput.value) {
    paramsDefault["search"] = searchInput.value;
  }
  if (entitiesInput.value) {
    paramsDefault["entities"] = entitiesInput.value.join();
  }
  if (tagsInput.value) {
    paramsDefault["tags"] = tagsInput.value.join();
  }
  paramsDefault["type"] = typeInput.value;
  paramsDefault["hidden"] = hiddenInput.value;

  paramsDefault.limit = import.meta.env.VITE_APP_MAXLIST;
  paramsDefault.offset =
    (currentPage.value - 1) * import.meta.env.VITE_APP_MAXLIST;
  return store.dispatch("materials/fetchMaterials", {
    params: { ...paramsDefault },
  });
}

onBeforeMount(async () => {
  loadPage();
  await store.dispatch("tags/fetchList",{params:{limit:1000}});
  await store.dispatch("entities/fetchList",{params:{limit:1000}});
  const list = await fetchList();
  loaded.value = true;
  return list;
});
</script>
