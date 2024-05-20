<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <h3 class="col-auto">Tags</h3>
            <div class="col-auto btn-group float-end" role="group">
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
                  <th>Nom</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in objects" :key="item.id">
                  <td v-text="item.name" />
                  <td class="text-end">
                    <router-link
                      class="btn btn-primary"
                      role="button"
                      :to="{
                        name: 'tag',
                        params: { tagid: item.id },
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
import { onBeforeMount, inject, ref } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/composables/useDebouncedRef";
import { useTagsStore } from "@/stores/tags";

import Pagination from "@/components/nav/ListPagination.vue";
import useSearchStorage from "@/composables/useSearchStorage";

const store = useTagsStore();
const loaded = ref(false);

const { objects, count: totalCount } = storeToRefs(store);

const confirmModal = inject("confirm");

async function destroyUnused() {
  const isConfirmed = await confirmModal({
    content: "Voulez vous vraiment supprimer tous les tags non utilisés ?",
  });
  if (isConfirmed) store.destroyUnused();
}

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
  "tags",
  fetch,
  { search: searchInput },
  currentPage,
  perPage.value
);

onBeforeMount(async () => {
  await refresh();
  loaded.value = true;
});
</script>
