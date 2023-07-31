import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";

export const usePurgeStore = defineStore("purge", () => {
    async function getDataArch(params) {
        try {
            const {data} = await ApiService.query("purge/dl_archive", params);
            return data;
        } catch (e) {
            console.log(e);
            return null;
        }
    }

    return {
        getDataArch,
    };
});
