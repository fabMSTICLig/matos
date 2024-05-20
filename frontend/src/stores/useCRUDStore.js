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

import { ref, computed } from "vue";
import ApiService from "@/helpers/api.service";

export default function useCRUDStore(ressource) {

  const objects = ref({});
  const count = ref(0);

  const list = computed(()=>Object.values(objects.value))


  function getById(id){
    return (id ? objects.value[id.toString()] : null);
  }
  async function fetchList(params = {}, prefix = "") {
    const { data } = await ApiService.query(prefix + ressource, params);
    objects.value={}
    data.results.forEach((m) => {
          objects.value[m["id"].toString()] = m;
        });
    count.value = data.count;

    return data.results;
  }
  async function fetchSingle(id, prefix = "" ) {
    if(Object.keys(objects.value).indexOf(id)>-1) return objects.value[id]

    const { data } = await ApiService.get(prefix + ressource, id);
    objects.value = { ...objects.value, [id]: data };
    return data;
  }
  async function create(dataIn, prefix = "") {
    const {data} = await ApiService.post(prefix + ressource, dataIn);
    objects.value = { ...objects.value, [data.id]: data };
    return data;
  }
  async function update(id, dataIn, prefix = "", params) {
    const {data} = await ApiService.update(prefix + ressource, id, dataIn, params);
    objects.value = { ...objects.value, [id]: data };
    return data;
  }
  async function destroy(id, prefix = "") {
    const { data } = await ApiService.delete(prefix + ressource, id);
    delete objects.value[id.toString()];
    return data;
  }

  return {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy}
}

