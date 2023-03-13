<template>
  <router-view v-if="loaded" />
</template>

<script>
export default {
  name: "MatosEntity",
};
</script>
<script setup>
import { ref, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, onBeforeRouteUpdate } from "vue-router";
import { useEntitiesStore } from "@/stores/entities";

const loaded = ref(false);
const store = useEntitiesStore();
const { currentEntity } = storeToRefs(store);

const route = useRoute();

async function initEntity(route) {
  const data = await store.fetchSingle(route.params.entityid);
  currentEntity.value = Object.assign({}, data);
  loaded.value = true;
}

onBeforeMount(async () => {
  await initEntity(route);
});
onBeforeRouteUpdate(async (to, from, next) => {
  if (to.params.entityid != from.params.entityid) await initEntity(to);
  next();
});
</script>
