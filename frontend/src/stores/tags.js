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
import useCRUDStore from "./useCRUDStore";

export const useTagsStore = defineStore("tags", () => {

  const {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy} = useCRUDStore("tags")

    async function destroyUnused() {
      const { data } = await ApiService.delete("tags/delete_unused");
      return data
    }

  return {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy, destroyUnused}
});
