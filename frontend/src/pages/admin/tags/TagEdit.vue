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
      <div v-if="object" class="card">
        <div class="card-header row justify-content-between">
          <h3 class="col-auto">
            Tags: <strong>{{ cardName }}</strong>
          </h3>
          <div class="col-auto btn-group float-end" role="group">
            <button
              v-if="!isNew"
              class="btn btn-danger"
              type="button"
              @click.prevent="destroy()"
            >
              Supprimer
            </button>
          </div>
        </div>
        <div class="card-body">
          <form ref="editorForm" class="row g-3">
            <div class="col-12">
              <label class="form-label" for="name">Name</label
              ><input
                id="name"
                v-model="object.name"
                class="form-control"
                type="text"
                required
              />
            </div>
            <div class="btn-group col-auto" role="group">
              <button
                v-if="isNew"
                class="btn btn-primary"
                type="button"
                @click.prevent="create()"
              >
                Ajouter
              </button>
              <button
                v-if="!isNew"
                class="btn btn-primary"
                type="button"
                @click.prevent="update()"
              >
                Modifier
              </button>
              <button
                class="btn btn-secondary"
                type="button"
                @click.prevent="cancel"
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";

import { useTagsStore } from "@/stores/tags";
import useEditor from "@/composables/useEditor";

const store = useTagsStore();

const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(store, { name: "" }, { name: "tags" });

const cardName = computed(() =>
  isNew.value ? "Nouveau tag" : object.value.name
);

const route = useRoute();

onBeforeMount(async () => {
  return initObject(route);
});
</script>
