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
        <div class="card-body">
          <form ref="editorForm" class="row g-3">
            <div class="col-12 col-md-6 border-end">
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
                <label class="form-label" for="quantity">Quantité</label
                ><input
                  id="quantity"
                  v-model="object.quantity"
                  class="form-control"
                  type="number"
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
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import { useGenericMaterialsStore } from "@/stores/materials";
import { useEntitiesStore } from "@/stores/entities";
import { useTagsStore } from "@/stores/tags";

import useEditor from "@/composables/useEditor";

import TagsInput from "@/components/ui/TagsInput.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const route = useRoute();
const prefix = "entities/" + route.params.entityid + "/";

const entitiesStore = useEntitiesStore();
const { currentEntity } = storeToRefs(entitiesStore);

const tagsStore = useTagsStore();
const { list: tagsList } = storeToRefs(tagsStore);

const showHelp = ref(false);

const store = useGenericMaterialsStore();
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

onBeforeMount(() => {
  return initObject(route);
});
</script>
