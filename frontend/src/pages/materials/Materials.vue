<template>
  <div>
    <h2>{{ name }}</h2>

    <router-view />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();

const name = computed(() => {
  let entity = store.getters["entities/byId"](route.params.entityid);
  if (entity) {
    return entity.name;
  } else return "";
});
</script>
