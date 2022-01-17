<template>
  <div class="row">
    <div class="col-12">
      <div v-if="object" class="card">
        <div class="card-header">
          <h3>{{ cardName }}</h3>
        </div>
        <div class="card-body">
          <form ref="editorForm" class="row g-3">
            <div class="col-12">
              <label class="form-label" for="name">Name</label>
              <input
                id="name"
                v-model="object.name"
                class="form-control"
                type="text"
                required
              />
            </div>

            <div class="col-12">
              <label class="form-label" for="type">Type</label>
              <select id="type" v-model="object.type" class="form-select">
                <option
                  v-for="(typename, type) in affiliationTypes"
                  :key="type"
                  :value="type"
                  v-text="typename"
                />
              </select>
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
                v-if="!isNew"
                class="btn btn-danger"
                type="button"
                @click.prevent="destroy()"
              >
                Supprimer
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
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";

const store = useStore();

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor("affiliations", { name: "", type: null }, "Affiliation");

const cardName = computed(() =>
  isNew.value ? "Nouvelle affiliation" : object.value.name
);
const affiliationTypes = computed(() => store.getters["affiliations/types"]);

const route = useRoute();

onBeforeMount(() => {
  store.dispatch("affiliations/fetchTypes").then(() => {
    return initObject(route);
  });
});
</script>
