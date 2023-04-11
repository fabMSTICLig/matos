<template>
  <div>
    <div v-if="object" class="card">
      <div class="card-header">
        <h3 class="float-start" v-text="cardName" />
        <div v-if="isAdmin" class="col-auto btn-group float-end" role="group">
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
              <label class="form-label" for="contact">Contact</label
              ><input
                id="contact"
                v-model="object.contact"
                class="form-control"
                type="email"
                required
              />
            </div>
            <div class="mb-3 form-check form-switch">
              <input
                id="check-active"
                v-model="object.is_pro"
                type="checkbox"
                class="form-check-input"
              />
              <label class="form-check-label" for="check-active"
                >Pro uniquement</label
              >
            </div>
            <div class="mb-3">
              <label class="form-label">Manageurs</label
              ><UserDynList v-model="object.managers"> </UserDynList>
              <div class="mb-3"></div>
              <label class="form-label">Affiliations</label>
              <DynList v-model="object.affiliations" :ressource="fetchAffs" />
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
            <div class="btn-group float-end" role="group">
              <button
                v-if="isNew"
                class="btn btn-primary"
                type="button"
                @click="create()"
              >
                Ajouter
              </button>
              <button
                v-if="!isNew"
                class="btn btn-primary"
                type="button"
                @click="update()"
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
</template>

<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useEntitiesStore } from "@/stores/entities";
import { useAffiliationsStore } from "@/stores/affiliations";

import useEditor from "@/composables/useEditor";

import UserDynList from "@/components/ui/UserDynList.vue";
import DynList from "@/components/ui/DynList.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const showHelp = ref(false);

const authStore = useAuthStore();
const { isAdmin } = storeToRefs(authStore);

const store = useEntitiesStore();
const {
  editorForm,
  object,
  isNew,
  initObject,
  create: createEditor,
  update: updateEditor,
  destroy: destroyEditor,
} = useEditor(
  store,
  {
    name: "",
    description: "",
    contact: "",
    affiliations: [],
    managers: [],
  },
  "entities"
);

const router = useRouter();
async function create() {
  const data = await createEditor(false);
  if (data.id)
    router.push({ name: "entityinfos", params: { entityid: data.id } });
}

async function update() {
  await updateEditor(false);
  router.push({ name: "entityinfos", params: route.params });
}
async function cancel() {
  router.push({ name: "entityinfos", params: route.params });
}
async function destroy() {
  await destroyEditor(false);
  router.push("/");
}

const storeAffiliations = useAffiliationsStore();
const { fetchList: fetchAffs } = storeAffiliations;

const cardName = computed(() =>
  isNew.value ? "Nouvelle Entité" : object.value.name
);

const route = useRoute();

onBeforeMount(() => {
  return initObject(route);
});
</script>
