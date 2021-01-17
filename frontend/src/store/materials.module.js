import Vue from "vue";
import ApiService from "@/common/api.service";
import createCrud from "@/common/storeCrudHelper";

const instances_extra = {};
const instances = createCrud("instances", instances_extra);

const specific_extra = {
  modules: {
    instances: instances
  }
};
export const specificmaterials = createCrud(
  "specificmaterials",
  specific_extra
);

const generic_extra = {};
export const genericmaterials = createCrud("genericmaterials", generic_extra);

export const materials = {
  namespaced: true,

  state: {
    specificmaterials: {},
    specificmaterialinstances: {},
    genericmaterials: {}
  },
  getters: {
    genericmaterials(state) {
      return state.genericmaterials;
    },
    gmById(state) {
      return id => (id ? state.genericmaterials[id.toString()] : null);
    },
    specificmaterials(state) {
      return state.specificmaterials;
    },
    smById(state) {
      return id => (id ? state.specificmaterials[id.toString()] : null);
    },
    specificmaterialinstances(state) {
      return state.specificmaterialinstances;
    },
    smiById(state) {
      return id => (id ? state.specificmaterialinstances[id.toString()] : null);
    }
  },
  actions: {
    searchMaterials(_, params) {
      return ApiService.query("materials/search", params).then(({ data }) => {
        return data;
      });
    },
    fetchMaterialsByLoans({ commit }, { loanids }) {
      return ApiService.query("materials/by_loans", {
        params: { loans: loanids.join() }
      })
        .then(({ data }) => {
          commit("fetchMaterialsBySuccess", data);
          return Promise.resolve(data);
        })
        .catch(error => {
          return Promise.reject(error);
        });
    },
    fetchMaterialsByIds(
      { commit },
      { gmids, smids } = { gmids: [], smids: [] }
    ) {
      return ApiService.query("materials/by_loans", {
        params: { gmids: gmids.join(), smids: smids.join() }
      })
        .then(({ data }) => {
          commit("fetchMaterialsBySuccess", data);
          return Promise.resolve(data);
        })
        .catch(error => {
          return Promise.reject(error);
        });
    }
  },

  mutations: {
    fetchMaterialsBySuccess(state, data) {
      data.generic_materials.forEach(m => {
        Vue.set(state.genericmaterials, m["id"].toString(), m);
      });
      data.specific_materials.forEach(m => {
        Vue.set(state.specificmaterials, m["id"].toString(), m);
      });
      data.specific_material_instances.forEach(m => {
        Vue.set(state.specificmaterialinstances, m["id"].toString(), m);
      });
    }
  }
};
