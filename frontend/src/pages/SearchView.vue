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
  <div>
    <div v-if="loaded" class="row">
      <div class="col-xl-3">
        <div class="card">
          <div class="card-header">
            <h4>Filtres</h4>
          </div>
          <div class="card-body">
            <form class="form">
              <div class="mb-3">
                <label class="form-label" for="searchInput">Chercher</label
                ><input
                  id="searchInput"
                  v-model="searchInput"
                  type="search"
                  class="form-control"
                  placeholder="Arduino"
                />
              </div>
              <div class="mb-3">
                <label class="form-label" for="typeInput">Type</label>
                <select id="typeInput" v-model="typeInput" class="form-control">
                  <option value="">Les deux</option>
                  <option value="g">Generique</option>
                  <option value="s">Specifique</option>
                </select>
              </div>

              <div v-if="toBasket" class="mb-3">
                <label class="form-label">Entités</label>
                <TagsInput
                  v-model="entitiesInput"
                  :ressource="entitiesList"
                  forbid-add
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Tags</label>
                <TagsInput
                  v-model="tagsInput"
                  :ressource="tagsList"
                  forbid-add
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
                />
                <label class="form-check-label" for="check-active"
                  >Invisible</label
                >
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            <h3 class="float-start">
              {{
                !toBasket
                  ? "Modification prêt" +
                    (!isAuthLoan
                      ? " [" + entities[pendingLoan.entity].name + "]"
                      : "") +
                    ": "
                  : ""
              }}Liste matériel
            </h3>
            <button
              v-if="!toBasket"
              class="btn btn-secondary float-end"
              @click="goBackToLoan"
            >
              Retour au prêt
            </button>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="item in materials"
                :key="item.name + item.id"
                class="list-group-item list-group-item-action flex-column align-items-start"
              >
                <div class="d-flex w-100 justify-content-between">
                  <a href="#" @click.prevent="goToMaterial(item)"
                    ><h4>{{ item.name }}</h4></a
                  >
                  <strong
                    ><router-link
                      :to="{
                        name: 'entityinfos',
                        params: { entityid: item.entity },
                      }"
                      >{{ entities[item.entity].name }}</router-link
                    ></strong
                  >
                </div>
                <markdown :description="item.description" :limit="3" />
                <p v-if="item.tags.length">
                  <strong>Tags :</strong>
                  <DisplayIdList :items="getTags(item.tags)" />
                </p>

                <button
                  v-if="!inLoan(item)"
                  class="btn btn-primary wt-1"
                  type="button"
                  :class="{
                    'disabled btn-secondary':
                      pendingLoan.entity && pendingLoan.entity != item.entity,
                  }"
                  @click="addItem(item)"
                >
                  Ajouter {{ toBasket ? "au panier" : "au prêt" }}
                </button>
                <button v-else class="btn btn-secondary" disabled>
                  Déjà dans le {{ toBasket ? "panier" : "prêt" }}
                </button>
                <div v-if="item.avail<=0" class="text-warning-emphasis" role="alert">
                  Non disponible aujourd'hui
                </div>
                <div v-if="item.avail != true && item.avail>0">
                  {{item.avail}} en stock aujourd'hui
                </div>
                <p
                    v-if="
                      pendingLoan.entity && pendingLoan.entity != item.entity
                    "
                  >
                  <small>Les matériels d'un prêt doivent tous appartenir à la même
                    entité</small
                  >
                </p>
              </li>
            </ul>
            <div class="mt-4 d-flex justify-content-center">
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
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useLoansStore } from "@/stores/loans";
import { useEntitiesStore } from "@/stores/entities";
import { useMaterialsStore } from "@/stores/materials";
import { useTagsStore } from "@/stores/tags";
import useDebouncedRef from "@/composables/useDebouncedRef";
import useSearchStorage from "@/composables/useSearchStorage";
import useLoanRouting from "@/composables/useLoanRouting";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";
import TagsInput from "@/components/ui/TagsInput.vue";
import Pagination from "@/components/nav/ListPagination.vue";

const route = useRoute();
const router = useRouter();

const toBasket = computed(() => route.name == "search");

const materialsStore = useMaterialsStore();
const {
  list: materials,
  count: totalCount,
} = storeToRefs(materialsStore);

const loaded = ref(false);
const authStore = useAuthStore();
const { authUser, isAdmin } = storeToRefs(authStore);

const loansStore = useLoansStore();
const { isAuthLoan, goBackToLoan } = useLoanRouting(loansStore, authUser);

const { basket, currentLoan } = storeToRefs(loansStore);

const pendingLoan = toBasket.value ? ref(basket) : ref(currentLoan);

const tagsStore = useTagsStore();
const { objects: tags, list: tagsList } = storeToRefs(tagsStore);

function getTags(tagids) {
  return tagids.map((id) => tags.value[id]);
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
  if (
    pendingLoan.value.entity == null &&
    entitiesInput.value.indexOf(item.entity) == -1
  ) {
    entitiesInput.value.push(item.entity);
  }
  loansStore.addMaterial(item, toBasket.value);
}

function inLoan(item) {
  if ("quantity" in item) {
    return (
      pendingLoan.value.generic_materials.find((mat) => {
        return mat.material == item.id;
      }) != undefined
    );
  } else {
    return item.id in pendingLoan.value.specific_materials;
  }
}

const entitiesStore = useEntitiesStore();
const { objects: entities, list: entitiesList } = storeToRefs(entitiesStore);

const searchInput = useDebouncedRef("");
const typeInput = ref("");
const entitiesInput = ref([]);
const tagsInput = ref([]);
const hiddenInput = ref(false);

const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

const { refresh, resetSearch } = useSearchStorage(
  route.name,
  fetch,
  {
    search: searchInput,
    type: typeInput,
    entities: entitiesInput,
    tags: tagsInput,
    hidden: hiddenInput,
  },
  currentPage,
  perPage.value
);
async function fetch(params) {
  await materialsStore.fetchMaterials(params);
}

onBeforeMount(async () => {
  if (route.name == "addmaterial" && loansStore.currentLoan == null)
    router.push("/");
  else {
    if (route.name == "addmaterial")
      entitiesInput.value.push(loansStore.currentLoan.entity);
    else {
      if ("entityid" in route.query) {
        let entid = parseInt(route.query.entityid);
        if (!isNaN(entid)) {
          resetSearch();
          entitiesInput.value.push(entid);
        }
        router.replace({ query: {} });
      }
    }
    await tagsStore.fetchList({ limit: 1000 });
    await entitiesStore.fetchList({ limit: 1000 });
    await refresh();
    loaded.value = true;
  }
});
</script>
