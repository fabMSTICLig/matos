<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-6">
              <input
                class="form-control"
                v-model="searchInput"
                type="search"
                placeholder="Search"
              />
            </div>
            <div class="col-auto">
              <div class="btn-group float-end" role="group">
                <router-link
                  class="btn btn-primary"
                  role="button"
                  :to="{ name: 'tag', params: { tagid: 'new' } }"
                >
                  Ajouter </router-link
                ><button
                  type="button"
                  class="btn btn-danger"
                  title="Supprimer les tags inutilisés"
                  @click="destroyUnused"
                >
                  Nettoyer
                </button>
              </div>
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
          <h3 class="float-start" v-text="selectedObject.name" />
          <div class="btn-group float-end" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'tag',
                params: { tagid: selectedObject.id },
              }"
            >
              Modifier
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            {{ selectedObject.name }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount, inject } from "vue";
import { useStore } from "vuex";

import useListFSP from "@/composables/useListFSP";
import Pagination from "@/components/nav/ListPagination.vue";

const store = useStore();

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
} = useListFSP("tags");

const confirmModal = inject("confirm");

async function destroyUnused() {
  const isConfirmed = await confirmModal({
    content: "Voulez vous vraiment supprimer tous les tags non utilisés ?",
  });
  if (isConfirmed) store.dispatch("tags/destroyUnused");
}

onBeforeMount(() => {
  loadPage();
  return fetchList();
});
</script>
