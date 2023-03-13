<template>
  <div class="row">
    <div class="col-12">
      <div v-if="object" class="card">
        <div class="card-header">
          <h3 class="float-start">
            {{ object.name }}
          </h3>
          <div v-if="isManager" class="btn-group float-end" role="group">
            <router-link
              class="btn btn-outline-primary"
              role="button"
              :to="{
                name: 'materialslist',
                params: { entityid: object.id },
              }"
            >
              Gestion Matériels
            </router-link>
            <router-link
              class="btn btn-outline-primary"
              role="button"
              :to="{
                name: 'entityloans',
                params: { entityid: object.id },
              }"
            >
              Gestion prêts
            </router-link>
            <!--<router-link
              class="btn btn-outline-primary"
              role="button"
              :to="{
                name: 'entity',
                params: { entityid: object.id },
              }"
            >
              Statistiques
            </router-link>-->
          </div>
        </div>
        <div class="card-body">
          <markdown :description="object.description" />
          <p class="card-text">
            <span><strong>Contact :&nbsp;</strong></span
            ><a :href="'mailto:' + object.contact">{{ object.contact }}</a>
          </p>
          <h4>Affiliations :&nbsp;</h4>
          <DisplayIdList :items="selectedAffiliations" />
          <router-link
            v-if="isManager"
            class="btn btn-primary btn-xl btn-circle position-absolute bottom-0 end-0"
            role="button"
            :to="{
              name: 'entityedit',
              params: { entityid: object.id },
            }"
          >
            <svg class="svg-icon">
              <use href="#edit" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useEntitiesStore } from "@/stores/entities";
import { useAuthStore } from "@/stores/auth";
import { useAffiliationsStore } from "@/stores/affiliations";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const authStore = useAuthStore();
const { isManager } =
  storeToRefs(authStore);

const store = useEntitiesStore();
const { currentEntity: object } = storeToRefs(store);

const affiliationsStore = useAffiliationsStore();
const { list: selectedAffiliations } = storeToRefs(affiliationsStore);

const route = useRoute();

onBeforeMount(async () => {
  loadAffiliations();
});
function loadAffiliations() {
  if (object.value) {
    if (object.value.affiliations)
      affiliationsStore.fetchList({ ids: object.value.affiliations.join(",") });
  }
}
watch(
  () => route.params.entityid,
  () => {
    loadAffiliations();
  }
);
</script>
