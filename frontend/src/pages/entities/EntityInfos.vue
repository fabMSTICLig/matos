<template>
  <div class="row">
    <div class="col-12">
      <div
        v-if="object"
        class="card"
      >
        <div class="card-header">
          <h3 class="float-start">
            {{ object.name }}
          </h3>
          <div
            class="btn-group float-end"
            role="group"
          >
            <router-link
              v-show="isManager"
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'entityedit',
                params: { entityid: object.id },
              }"
            >
              Modifier
            </router-link>
            <router-link
              v-if="isManager"
              class="btn btn-primary float-end"
              role="button"
              :to="{
                name: 'entitieslist',
              }"
            >
              Retour
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <fieldset>
            <legend>Informations</legend>
            <markdown
              :description="object.description"
            />
            <p class="card-text">
              <span><strong>Contact :&nbsp;</strong></span><a :href="'mailto:' + object.contact">{{ object.contact }}</a>
            </p>
            <h4>Affiliations :&nbsp;</h4>
            <DisplayIdList :items="selectedAffiliations" />
          </fieldset>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";
import Markdown from "@/components/ui/Markdown.vue";

const store = useStore();
const authUser = computed(() => store.getters["authUser"]);
const isManager = computed(() => {
  return (
    (object.value && authUser.value.entities.indexOf(object.value.id) > -1) ||
    authUser.value.is_staff
  );
});

const { object, initObject } = useEditor("entities", {}, "Entité");

const selectedAffiliations = computed(() => store.getters["affiliations/list"]);
watch(object, () => {
  if (object.value) {
    if (object.value.affiliations)
      store.dispatch("affiliations/fetchList", {
        params: { ids: object.value.affiliations.join(",") },
      });
  }
});
const route = useRoute();
onBeforeMount(() => {
  return initObject(route);
});
</script>
