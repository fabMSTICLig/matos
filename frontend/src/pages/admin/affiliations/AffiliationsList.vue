<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-auto">
              <h3>Applications</h3>
            </div>
            <div class="col-auto">
              <router-link
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'affiliation', params: { affid: 'new' } }"
              >
                Ajouter
              </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <form class="row row-cols-lg-auto g-3 align-items-center">
            <div class="col-12">
              <label class="form-label visually-hidden" for="searchInput"
                >Chercher</label
              >
              <input
                id="searchInput"
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              />
            </div>
          </form>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Nom</th>
                  <th></th>
                </tr>
              </thead>
              <tbody v-if="loaded">
                <tr v-for="item in objects" :key="item.id">
                  <td v-text="affiliationTypes[item.type]" />
                  <td v-text="item.name" />
                  <td class="text-end">
                    <router-link
                      class="btn btn-primary"
                      role="button"
                      :to="{
                        name: 'affiliation',
                        params: { affid: item.id },
                      }"
                    >
                      Modifier
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/composables/useDebouncedRef";

import { useAffiliationsStore } from "@/stores/affiliations";
import Pagination from "@/components/nav/ListPagination.vue";
import useSearchStorage from "@/composables/useSearchStorage";

const store = useAffiliationsStore();
const loaded = ref(false);

const {
  objects,
  count: totalCount,
  types: affiliationTypes,
} = storeToRefs(store);

const searchInput = useDebouncedRef("");
const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

async function fetch(params) {
  await store.fetchList({ ...params });
}

const { refresh } = useSearchStorage(
  "affiliations",
  fetch,
  { search: searchInput },
  currentPage,
  perPage.value
);

onBeforeMount(async () => {
  await store.fetchTypes();
  await refresh();
  loaded.value = true;
});
</script>
