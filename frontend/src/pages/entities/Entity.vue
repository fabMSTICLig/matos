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
