<template>
  <div>
    <div
      v-if="object"
      class="card"
    >
      <div class="card-header">
        <h3
          class="float-start"
          v-text="cardName"
        />
        <div
          v-if="!isNew"
          class="btn-group float-end"
          role="group"
        >
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'materialslist',
              params: { entityid: object.id },
            }"
          >
            Matériels
          </router-link>
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'entityloans',
              params: { entityid: object.id },
            }"
          >
            Prêts
          </router-link>
        </div>
      </div>
      <div class="card-body">
        <form
          ref="editorForm"
          class="row g-3"
        >
          <div class="col-12 col-md-6">
            <fieldset>
              <legend>Informations</legend>
              <div class="mb-3">
                <label
                  class="form-label"
                  for="name"
                >Nom</label><input
                  id="name"
                  v-model="object.name"
                  class="form-control"
                  type="text"
                  required
                >
              </div>
              <div class="mb-3">
                <label
                  class="form-label"
                  for="contact"
                >Contact</label><input
                  id="contact"
                  v-model="object.contact"
                  class="form-control"
                  type="email"
                  required
                >
              </div>
              <div class="mb-3">
                <label
                  class="form-label"
                  for="description"
                >Description</label>
                <textarea
                  id="description"
                  v-model="object.description"
                  rows="3"
                  class="form-control"
                />
                <a
                  href="#"
                  @click.prevent="showHelp = true"
                >Aide</a>
              </div>
            </fieldset>
          </div>

          <div class="col-12 col-md-6">
            <markdown
              v-model:showHelp="showHelp"
              :description="object.description"
            />
          </div>

          <div class="col-12 col-md-6">
            <fieldset>
              <legend>Managers</legend>
              <div class="mb-3">
                <DynList
                  v-model="object.managers"
                  ressource="users"
                  :make-label="makeUserLabel"
                >
                  <template #default="slotProps">
                    <strong>@{{ slotProps.item.username }} :</strong>
                    {{ slotProps.item.first_name }}
                    {{ slotProps.item.last_name }}
                  </template>
                </DynList>
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
          <div class="row">
            <div
              class="btn-group col-auto"
              role="group"
            >
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
</template>

<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";

import DynList from "@/components/ui/DynList.vue";
import Markdown from "@/components/ui/Markdown.vue";

const showHelp = ref(false);

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor(
    "entities",
    {
      name: "",
      description: "",
      contact: "",
      affiliations: [],
      managers: [],
    },
    "Entité"
  );

function makeUserLabel(u) {
  return "@" + u.username + " " + u.first_name + " " + u.last_name;
}

const cardName = computed(() =>
  isNew.value ? "Nouvelle Entité" : object.value.name
);

const route = useRoute();

onBeforeMount(() => {
  return initObject(route);
});
</script>
