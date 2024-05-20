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
import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";
import useCRUDStore from "./useCRUDStore";

export const useSpecificMaterialsStore = defineStore(
  "specificMaterials",
  () => {
    const {
      objects,
      count,
      list,
      getById,
      fetchList,
      fetchSingle,
      create,
      update,
      destroy,
    } = useCRUDStore("specificmaterials");

    async function createInstance(dataI, prefix = "") {
      const { data } = await ApiService.post(
        prefix + "specificmaterials/" + dataI.model + "/instances",
        dataI
      );
      const model = data["model"].toString();
      objects.value[model].instances.push(data);
      return data;
    }
    async function updateInstance(id, dataI, prefix = "") {
      const { data } = await ApiService.update(
        prefix + "specificmaterials/" + dataI.model + "/instances",
        id,
        dataI
      );
      if (data["id"]) {
        const model = data["model"].toString();
        const listIndex = objects.value[model].instances.findIndex(
          (e) => e.id == data["id"]
        );
        if (listIndex >= 0) {
          objects.value[model].instances.splice(listIndex, 1, data);
        }
      }
      return data;
    }
    async function destroyInstance(id, model, prefix = "") {
      const { data } = await ApiService.delete(
        prefix + "specificmaterials/" + model + "/instances",
        id
      );
      const listIndex = objects.value[model.toString()].instances.findIndex(
        (e) => e.id == id
      );
      if (listIndex >= 0) {
        objects.value[model.toString()].instances.splice(listIndex, 1);
      }
      return data;
    }

    return {
      objects,
      count,
      list,
      getById,
      fetchList,
      fetchSingle,
      create,
      update,
      destroy,
      createInstance,
      updateInstance,
      destroyInstance,
    };
  }
);

export const useGenericMaterialsStore = defineStore("genericMaterials", () => {
  return useCRUDStore("genericmaterials");
});

export const useMaterialsStore = defineStore("materials", () => {
  const specificmaterials = ref({});
  const genericmaterials = ref({});
  const count = ref(0);
  const list = computed(() =>
    Object.values(genericmaterials.value).concat(
      Object.values(specificmaterials.value)
    )
  );

  function fetchMaterialSuccess(data) {
    let genmat = {};
    data.results.generic_materials.forEach((m) => {
      genmat[m["id"].toString()] = m;
    });
    genericmaterials.value = genmat;
    let spemat = {};
    data.results.specific_materials.forEach((m) => {
      spemat[m["id"].toString()] = m;
    });
    specificmaterials.value = spemat;
    count.value = data.count;
  }

  async function fetchMaterials(params, prefix = "") {
    const { data } = await ApiService.query(prefix + "materials", params);
    fetchMaterialSuccess(data);
    return list.value;
  }
  async function fetchMaterialsByLoan(loanid) {
    const { data } = await ApiService.query("materials", {
      loan: loanid,
    });
    fetchMaterialSuccess(data);
    return list.value;
  }
  async function fetchMaterialsByIds(gmids = [], smids = []) {
    const { data } = await ApiService.query("materials", { gmids: gmids.join(), smids: smids.join(), hidden:true });
    fetchMaterialSuccess(data);
    return list.value;
  }
  async function fetchSingleGenericMaterial(id) {
    const { data } = await ApiService.get("materials/g", id);
    return data;
  }
  async function fetchSingleSpecificMaterial(id) {
    const { data } = await ApiService.get("materials/s", id);
    return data;
  }

  return {
    genericmaterials,
    specificmaterials,
    count,
    list,
    fetchMaterials,
    fetchMaterialsByLoan,
    fetchMaterialsByIds,
    fetchSingleGenericMaterial,
    fetchSingleSpecificMaterial,
  };
});
