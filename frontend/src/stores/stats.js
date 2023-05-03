import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";

export const useStatsStore = defineStore("stats", () => {
    async function getDataPage(type, params) {
        try {
            const data = await ApiService.query("stats/" + type, params);
            return data["data"];
        } catch (e) {
            console.log(e);
            return null;
        }
    }

    return {
        getDataPage,
    };
});