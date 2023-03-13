
import { ref } from "vue";
import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useEntitiesStore = defineStore("entities", () => {

  const currentEntity = ref({});


  return { ...useCRUDStore("entities"), currentEntity }
});
