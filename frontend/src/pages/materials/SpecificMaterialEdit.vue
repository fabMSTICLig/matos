<template>
  <div class="row">
    <div class="col-12">
      <div
        v-if="object"
        class="card"
      >
        <div class="card-header">
          <h3 v-text="cardName" />
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-12 col-md-4">
              <form
                ref="editorForm"
                class="row g-3"
              >
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
                      for="description"
                    >Description</label><textarea
                      id="description"
                      v-model="object.description"
                      rows="5"
                      class="form-control"
                    />
                    <a
                      href="#"
                      @click.prevent="showHelp = true"
                    >Aide</a>
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="refInt"
                    >Référence interne</label><input
                      id="refInt"
                      v-model="object.ref_int"
                      class="form-control"
                      type="text"
                    >
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="refMan"
                    >Référence fabriquant</label><input
                      id="refMan"
                      v-model="object.ref_man"
                      class="form-control"
                      type="text"
                    >
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="localisation"
                    >Localisation</label><input
                      id="localisation"
                      v-model="object.localisation"
                      class="form-control"
                      type="text"
                    >
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Tags</label>
                    <TagsInput
                      v-model="object.tags"
                      ressource="tags"
                    />
                  </div>
                  <div class="mb-3 form-check form-switch">
                    <input
                      id="check-active"
                      v-model="object.active"
                      type="checkbox"
                      class="form-check-input"
                    >
                    <label
                      class="form-check-label"
                      for="check-active"
                    >Visible</label>
                  </div>
                </fieldset>
              </form>
              <div
                class="btn-group"
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
            <div class="col-12 col-md-8">
              <div class="row">
                <div class="col-12 col-md-6">
                  <fieldset>
                    <legend>Instances</legend>
                    <form
                      ref="editorInstances"
                      @submit.prevent="addInstance"
                    >
                      <div class="input-group">
                        <span class="input-group-text">Ajouter</span>
                        <input
                          v-model="newInstanceName"
                          class="form-control"
                          required
                        >
                        <button
                          class="btn btn-primary"
                          type="submit"
                        >
                          Valider
                        </button>
                      </div>
                    </form>
                    <ul class="list-group">
                      <li
                        v-for="item in object.instances"
                        :key="item.id"
                        class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                        :class="{
                          active:
                            selectedInstance && item.id == selectedInstance.id,
                        }"
                        @click="selectInstance(item)"
                      >
                        <span>
                          {{ item.name }}
                        </span>
                        <button
                          class="btn btn-danger"
                          type="button"
                          @click.prevent="removeInstance(item)"
                        >
                          X
                        </button>
                      </li>
                    </ul>
                  </fieldset>
                </div>
                <div class="col-12 col-md-6">
                  <div v-if="!isNew && selectedInstance">
                    <form
                      class="row g-3"
                      @submit.prevent="updateInstance"
                    >
                      <fieldset>
                        <legend>Instance</legend>
                        <div class="mb-3">
                          <label
                            class="form-label"
                            for="nameI"
                          >Nom</label><input
                            id="nameI"
                            v-model="selectedInstance.name"
                            class="form-control"
                            type="text"
                            required
                          >
                        </div>
                        <div class="mb-3">
                          <label
                            class="form-label"
                            for="serialNumI"
                          >Numéro série</label><input
                            id="serialNumI"
                            v-model="selectedInstance.serial_num"
                            class="form-control"
                            type="text"
                          >
                        </div>
                        <div class="mb-3">
                          <label
                            class="form-label"
                            for="descriptionI"
                          >Description</label>
                          <textarea
                            id="descriptionI"
                            v-model="selectedInstance.description"
                            rows="3"
                            class="form-control"
                          />
                        </div>
                        <div class="mb-3 form-check form-switch">
                          <input
                            id="check-active-instance"
                            v-model="selectedInstance.active"
                            type="checkbox"
                            class="form-check-input"
                          >
                          <label
                            class="form-check-label"
                            for="check-active-instance"
                          >Visible</label>
                        </div>
                      </fieldset>
                      <div class="row">
                        <div
                          class="btn-group col-auto"
                          role="group"
                        >
                          <button
                            class="btn btn-primary"
                            type="submit"
                          >
                            Modifier
                          </button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <div class="row mt-4">
              <div class="col-12">
                <h4>Aperçu description</h4>
                <markdown
                  v-if="object.description"
                  v-model:showHelp="showHelp"
                  :description="object.description"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, inject, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";

import TagsInput from "@/components/ui/TagsInput.vue";
import Markdown from "@/components/ui/Markdown.vue";

const store = useStore();
const route = useRoute();

const showHelp = ref(false);

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor(
    "specificmaterials",
    {
      name: "",
      ref_int: null,
      ref_man: null,
      localisation: null,
      description: "",
      instances: [],
      entity: route.params["entityid"],
      tags: [],
      active: true,
    },
    "Matériel spécifique",
    { prefix: "entities/" + route.params.entityid + "/" }
  );

const cardName = computed(() =>
  isNew.value ? "Nouveau matériel" : object.value.name
);

const newInstanceName = ref("");
const selectedInstance = ref(null);

function selectInstance(instance) {
  selectedInstance.value = Object.assign({}, instance);
}

const showModal = inject("show");

async function addInstance() {
  const instance = await store.dispatch("specificmaterials/createInstance", {
    data: {
      name: newInstanceName.value,
      model: object.value.id,
      serial_num: null,
    },
    prefix: "entities/" + route.params.entityid + "/",
  });
  newInstanceName.value = "";
  selectInstance(instance);
  showModal({ content: "Instance crée" });
}
async function updateInstance() {
  console.log(store);
  const instance = await store.dispatch("specificmaterials/updateInstance", {
    id: selectedInstance.value.id,
    data: selectedInstance.value,
    prefix: "entities/" + route.params.entityid + "/",
  });
  selectInstance(instance);
  showModal({ content: "Instance mise à jour" });
}
async function removeInstance(instance) {
  await store.dispatch("specificmaterials/destroyInstance", {
    model: object.value.id,
    id: instance.id,
    prefix: "entities/" + route.params.entityid + "/",
  });
  if (instance.id == selectedInstance.value.id) {
    selectedInstance.value = null;
  }
  showModal({ content: "Instance supprimée" });
}
onBeforeMount(async () => {
  await initObject(route);
});
</script>
