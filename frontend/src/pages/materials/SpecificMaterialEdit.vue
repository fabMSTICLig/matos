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
        <div class="card-header">
          <h3 class="float-start">
            <h3>{{ currentEntity.name }}: {{ cardName }}</h3>
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
        <div class="card-body row">
          <div class="col-12 col-md-6 border-end">
            <form ref="editorForm" class="g-3">
              <div class="mb-3">
                <label class="form-label" for="name">Nom</label
                ><input
                  id="name"
                  v-model="object.name"
                  class="form-control"
                  type="text"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label" for="refInt">Référence interne</label
                ><input
                  id="refInt"
                  v-model="object.ref_int"
                  class="form-control"
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label" for="refMan"
                  >Référence fabriquant</label
                ><input
                  id="refMan"
                  v-model="object.ref_man"
                  class="form-control"
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label" for="localisation">Localisation</label
                ><input
                  id="localisation"
                  v-model="object.localisation"
                  class="form-control"
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Tags</label>
                <TagsInput
                  v-model="object.tags"
                  :ressource="tagsList"
                  :create="tagsStore.create"
                />
              </div>
              <div class="mb-3 form-check form-switch">
                <input
                  id="check-active"
                  v-model="object.active"
                  type="checkbox"
                  class="form-check-input"
                />
                <label class="form-check-label" for="check-active"
                  >Visible</label
                >
              </div>
            </form>
            <div v-if="!isNew" class="mb-3">
              <form
                ref="addForm"
                class="needs-validation"
                @submit.prevent="addInstance"
              >
                <div class="input-group has-validation">
                  <span class="input-group-text">Ajouter</span>
                  <input
                    v-model="newInstanceName"
                    class="form-control"
                    :class="{ 'is-invalid': newInstanceError }"
                    required
                    @input="newInstanceError = false"
                  />
                  <button class="btn btn-primary" type="submit">Valider</button>
                  <div class="invalid-feedback">
                    Une instance possède déjà ce nom
                  </div>
                </div>
              </form>
              <ul class="list-group">
                <li
                  v-for="item in object.instances"
                  :key="item.id"
                  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                  :class="{
                    active: selectedInstance && item.id == selectedInstance.id,
                  }"
                  @click="selectInstance(item)"
                >
                  <span>
                    {{ item.name }}
                  </span>
                  <button
                    class="btn btn-danger"
                    type="button"
                    @click.stop="removeInstance(item)"
                  >
                    X
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-12 col-md-6">
            <div class="mb-3">
              <label class="form-label" for="description">Description</label>
              <textarea
                id="description"
                v-model="object.description"
                rows="3"
                class="form-control"
              />
              <a href="#" @click.prevent="showHelp = true">Aide</a>
            </div>
            <h4>Aperçu description</h4>
            <hr />
            <markdown
              v-model:showHelp="showHelp"
              :description="object.description"
            />
          </div>
          <div class="col-12">
            <div class="float-end">
              <div class="btn-group" role="group">
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
                  @click.prevent="cancel()"
                >
                  Annuler
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <modal
        id="modal-instance"
        :show="selectedInstance != null"
        :resolve="
          () => {
            selectedInstance = null;
          }
        "
        title="Instance"
        hide-footer
      >
        <form class="row g-3" @submit.prevent="updateInstance">
          <div class="mb-3">
            <label class="form-label" for="nameI">Nom</label
            ><input
              id="nameI"
              v-model="selectedInstance.name"
              class="form-control"
              type="text"
              required
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="serialNumI">Numéro série</label
            ><input
              id="serialNumI"
              v-model="selectedInstance.serial_num"
              class="form-control"
              type="text"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="descriptionI">Description</label>
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
            />
            <label class="form-check-label" for="check-active-instance"
              >Visible</label
            >
          </div>
          <div class="col-12">
            <div class="btn-group float-end" role="group">
              <button class="btn btn-primary" type="submit">Modifier</button>
              <button
                class="btn btn-secondary"
                type="button"
                @click.prevent="selectedInstance = null"
              >
                Annuler
              </button>
            </div>
          </div>
        </form>
      </modal>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { useSpecificMaterialsStore } from "@/stores/materials";
import { useEntitiesStore } from "@/stores/entities";
import { useTagsStore } from "@/stores/tags";

import useEditor from "@/composables/useEditor";

import TagsInput from "@/components/ui/TagsInput.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";
import Modal from "@/plugins/modal";

const route = useRoute();
const prefix = "entities/" + route.params.entityid + "/";

const entitiesStore = useEntitiesStore();
const { currentEntity } = storeToRefs(entitiesStore);

const tagsStore = useTagsStore();
const { list: tagsList } = storeToRefs(tagsStore);

const showHelp = ref(false);

const store = useSpecificMaterialsStore();
const {
  editorForm,
  object,
  isNew,
  initObject,
  create: createEditor,
  update,
  destroy,
  cancel,
} = useEditor(
  store,
  {
    name: "",
    ref_int: null,
    ref_man: null,
    localisation: null,
    description: "",
    quantity: 0,
    entity: route.params["entityid"],
    tags: [],
    active: true,
  },
  { name: "materialslist" },
  { prefix }
);
const cardName = computed(() =>
  isNew.value ? "Nouveau matériel" : object.value.name
);

const router = useRouter();
async function create() {
  if (!isNew.value) createEditor();
  else {
    const data = await createEditor(false);
    router.push({ name: "specificmaterial", params: { matid: data.id } });
  }
}

onBeforeMount(() => {
  return initObject(route);
});
const addForm = ref();
const newInstanceName = ref("");
const newInstanceError = ref(false);
const selectedInstance = ref(null);

function selectInstance(instance) {
  selectedInstance.value = Object.assign({}, instance);
}

async function addInstance() {
  if (addForm.value.checkValidity()) {
    try {
      await store.createInstance(
        {
          name: newInstanceName.value,
          model: object.value.id,
          serial_num: null,
        },
        prefix
      );
      newInstanceName.value = "";
    } catch (error) {
      if (error.response && error.response.status == 400) {
        newInstanceError.value = true;
      }
    }
  } else {
    addForm.value.reportValidity();
  }
}
async function updateInstance() {
  await store.updateInstance(
    selectedInstance.value.id,
    selectedInstance.value,
    prefix
  );
  selectedInstance.value = null;
}
async function removeInstance(instance) {
  await store.destroyInstance(instance.id, object.value.id, prefix);
}
</script>
