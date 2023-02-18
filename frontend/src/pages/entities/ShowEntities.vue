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
                  v-for="item in objects"
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
            :total="totalCount"
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
             <router-link
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'search', query: { entityid: selectedObject.id } }"
              >
             Voir le matériels
              </router-link>
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
import { ref, onBeforeMount, watch } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/composables/useDebouncedRef";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

import { useEntitiesStore } from "@/stores/entities";
import { useAffiliationsStore } from "@/stores/affiliations";
import Pagination from "@/components/nav/ListPagination.vue";
import useSearchStorage from "@/composables/useSearchStorage";

const store = useEntitiesStore();
const loaded = ref(false);

const {
  objects,
  count: totalCount,
} = storeToRefs(store);

const searchInput = useDebouncedRef("");
const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

async function fetch(params) {
  const list = await store.fetchList({ ...params });
  if(list.length)
  {
    selectedObject.value=list[0];
  }
}

const { refresh } = useSearchStorage(
  "entities",
  fetch,
  { search: searchInput },
  currentPage,
  perPage.value
);

const selectedObject = ref({})

const storeAffiliations = useAffiliationsStore();
const {
  list:selectedAffiliations,
} = storeToRefs(storeAffiliations);

watch(selectedObject, () => {
  if (selectedObject.value) {
    if (selectedObject.value.affiliations)
      storeAffiliations.fetchList({ ids: selectedObject.value.affiliations.join(",") });
  }
});

onBeforeMount(async () => {
  await refresh();
  loaded.value = true;
});
</script>
