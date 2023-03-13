import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";
import useCRUDStore from "./useCRUDStore";

export const useAffiliationsStore = defineStore("affiliations", () => {

  const types = ref({});

    async function fetchTypes() {
      const { data } = await ApiService.query("affiliations/types", {});
      types.value=data
      return data;
    }

  return { ...useCRUDStore("affiliations"), types, fetchTypes }
});
