/*
 * Copyright (C) 2020-2024 LIG Université Grenoble Alpes
 *
 *
 * This file is part of Matos.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * Matos is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
 * @author Clément Lesaulnier
 * @author Robin Courault
*/
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