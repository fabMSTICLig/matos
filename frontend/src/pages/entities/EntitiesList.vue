<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-6">
              <input
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              >
            </div>
            <div class="col-auto">
              <router-link
                v-if="authUser.is_staff"
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'entityedit', params: { entityid: 'new' } }"
              >
                Ajouter
              </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Nom</th>
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
      <div
        v-if="selectedObject"
        class="card"
      >
        <div class="card-header">
          <h3
            class="float-start"
            v-text="selectedObject.name"
          />
          <div
            class="btn-group float-end"
            role="group"
          >
            <button
              v-show="isManager"
              class="btn btn-primary"
              @click="toRoute('entityedit')"
            >
              Modifier
            </button>
            <button
              v-show="isManager"
              class="btn btn-primary"
              @click="toRoute('materialslist')"
            >
              Matériels
            </button>
            <button
              v-show="isManager"
              class="btn btn-primary"
              @click="toRoute('entityloans')"
            >
              Prêts
            </button>
          </div>
        </div>
        <div class="card-body">
          <markdown :description="selectedObject.description" />
          <p class="card-text">
            <span><strong>Contact :&nbsp;</strong></span><a :href="'mailto:' + selectedObject.contact">{{
              selectedObject.contact
            }}</a>
          </p>
          <h5>Affiliations</h5>
          <DisplayIdList :items="selectedAffiliations" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/Markdown.vue";

import useListFSP from "@/composables/useListFSP";
import Pagination from "@/components/nav/ListPagination.vue";

const {
  selectedObject,
  searchInput,
  currentPage,
  pagesCount,
  perPage,
  onPageChange,
  loadPage,
  objectsList,
  objectsCount,
  fetchList,
} = useListFSP("entities");

const store = useStore();

const authUser = computed(() => store.getters["authUser"]);
const isManager = computed(() => {
  return (
    selectedObject.value &&
    (authUser.value.entities.indexOf(selectedObject.value.id) > -1 ||
      authUser.value.is_staff)
  );
});

const selectedAffiliations = computed(() => store.getters["affiliations/list"]);

watch(selectedObject, () => {
  if (selectedObject.value) {
    if (selectedObject.value.affiliations)
      store.dispatch("affiliations/fetchList", {
        params: { ids: selectedObject.value.affiliations.join(",") },
      });
  }
});
const router = useRouter();
function toRoute(route) {
  router.push({ name: route, params: { entityid: selectedObject.value.id } });
}

onBeforeMount(() => {
  loadPage();
  return fetchList();
});
</script>
