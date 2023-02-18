<template>
  <div class="row">
    <div class="col-12">
      <div v-if="object" class="card">
        <div class="card-header row justify-content-between">
          <h3 class="col-auto">
            Users: <strong>{{ cardName }}</strong>
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
                    :ressource="fetchAffiliations"
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Entités</legend>
                <div class="mb-3">
                  <DynList
                    v-model="object.entities"
                    :ressource="fetchEntities"
                  />
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
                  class="btn btn-secondary"
                  type="button"
                  @click.prevent="cancel"
                >
                  Annuler
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
import DynList from "@/components/ui/DynList.vue";
import { computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";

import { useUsersStore } from "@/stores/users";
import { useAffiliationsStore } from "@/stores/affiliations";
import { useEntitiesStore } from "@/stores/entities";
import useEditor from "@/composables/useEditor";

const store = useUsersStore();
const { fetchList: fetchAffiliations } = useAffiliationsStore();
const { fetchList: fetchEntities } = useEntitiesStore();

const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(
  store,
  {
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    users: [],
  },
  { name: "users" }
);

const cardName = computed(() =>
  isNew.value ? "Nouvel utilisateur" : object.value.username
);

const route = useRoute();

onBeforeMount(async () => {
  return initObject(route);
});
</script>
