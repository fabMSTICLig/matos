import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";
import useCRUDStore from "./useCRUDStore";

export const useTagsStore = defineStore("tags", () => {

  const {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy} = useCRUDStore("tags")

    async function destroyUnused() {
      const { data } = await ApiService.delete("tags/delete_unused");
      return data
    }

  return {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy, destroyUnused}
});
