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
                  <label class="form-label" for="refMan">Référence fabriquant</label
                ><input
                    id="refMan"
                    v-model="object.ref_man"
                    class="form-control"
                    type="text"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="description">Description</label
                ><textarea
                    id="description"
                    rows="5"
                    v-model="object.description"
                    class="form-control"
                  />
                  <a href="#" @click.prevent="showHelp = true">Aide</a>
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
                  <TagsInput v-model="object.tags" ressource="tags" />
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
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <h4>Aperçu description</h4>
              <markdown
                v-if="object.description"
                :description="object.description"
                v-model:showHelp="showHelp"
              />
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
import { ref, computed, onBeforeMount } from "vue";
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
    "genericmaterials",
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
    "Matériel générique",
    { prefix: "entities/" + route.params.entityid + "/" }
  );

const cardName = computed(() =>
  isNew.value ? "Nouveau matériel" : object.value.name
);

onBeforeMount(() => {
  return initObject(route);
});
</script>
