<template>
  <div class="row">
    <div class="col-12">
      <div v-if="object" class="card">
        <div class="card-header">
          <h3 v-text="cardName" />
        </div>
        <div class="card-body">
          <form ref="editorForm" class="row g-3">
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Informations</legend>
                <div class="mb-3">
                  <label class="form-label">Nom utilisateur</label
                  ><input
                    v-model="object.username"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Prénom</label
                  ><input
                    v-model="object.first_name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Nom</label
                  ><input
                    v-model="object.last_name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Email</label
                  ><input
                    v-model="object.email"
                    class="form-control"
                    type="email"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">RGPD accept date</label
                  ><input
                    v-model="object.rgpd_accept"
                    class="form-control"
                    type="date"
                    readonly
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Affiliations</legend>
                <div class="mb-3">
                  <DynList
                    v-model="object.affiliations"
                    ressource="affiliations"
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Entités</legend>
                <div class="mb-3">
                  <DynList v-model="object.entities" ressource="entities" />
                </div>
              </fieldset>
            </div>
            <div class="row">
            <div class="btn-group col-auto" role="group">
              <button
                v-if="isNew"
                class="btn btn-primary"
                type="button"
                @click="create"
              >
                Ajouter
              </button>
              <button
                v-if="!isNew"
                class="btn btn-primary"
                type="button"
                @click="update(msg)"
              >
                Modifier
              </button>
              <button
                v-if="!isNew"
                class="btn btn-danger"
                type="button"
                @click="destroy"
              >
                Supprimer
              </button>
            </div>
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

import DynList from "@/components/ui/DynList.vue";

const store = useStore();

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor(
    "users",
    {
      username: "",
      first_name: "",
      last_name: "",
      email: "",
      affiliations: [],
    },
    "User"
  );

const cardName = computed(() =>
  isNew.value ? "Nouvel Utilisateur" : object.value.username
);

const route = useRoute();

onBeforeMount(() => {
  return initObject(route);
});
</script>
