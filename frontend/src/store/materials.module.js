import createCrud from "./crud.factory";
import ApiService from "../common/api.service";

const specific_extra = {
  actions: {
    async createInstance({ commit }, { data, prefix = "" }) {
      const response = await ApiService.post(
        prefix + "specificmaterials/" + data.model + "/instances",
        data
      );
      commit("createInstanceSuccess", response.data);
      return response.data;
    },
    async updateInstance({ commit }, { id, data, prefix = "" }) {
      const response = await ApiService.update(
        prefix + "specificmaterials/" + data.model + "/instances",
        id,
        data
      );
      commit("updateInstanceSuccess", response.data);
      return response.data;
    },
    async destroyInstance({ commit }, { id, model, prefix = "" }) {
      const { data } = await ApiService.delete(
        prefix + "specificmaterials/" + model + "/instances",
        id
      );
      commit("destroyInstanceSuccess", { model, id });
      return data;
    },
  },

  mutations: {
    createInstanceSuccess(state, data) {
      if (data) {
        const model = data["model"].toString();
        state.entities[model].instances.push(data);
      }
    },
    updateInstanceSuccess(state, data) {
      if (data["id"]) {
        const model = data["model"].toString();
        const listIndex = state.entities[model].instances.findIndex(
          (e) => e.id == data["id"]
        );
        if (listIndex >= 0) {
          state.entities[model].instances.splice(listIndex, 1, data);
        }
      }
    },
    destroyInstanceSuccess(state, { model, id }) {
      const listIndex = state.entities[model.toString()].instances.findIndex(
        (e) => e.id == id
      );
      if (listIndex >= 0) {
        state.entities[model.toString()].instances.splice(listIndex, 1);
      }
    },
  },
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
    genericmaterials: {},
    count: 0,
  },
  getters: {
    genericmaterials(state) {
      return state.genericmaterials;
    },
    specificmaterials(state) {
      return state.specificmaterials;
    },
    list(state) {
      return Object.values(state.genericmaterials).concat(
        Object.values(state.specificmaterials)
      );
    },
  },
  actions: {
    async fetchMaterials({ commit, getters }, { params, prefix = "" }) {
      const { data } = await ApiService.query(prefix + "materials", params);
      commit("fetchMaterialsSuccess", data);
      return getters.list;
    },
    async fetchMaterialsByLoan({ commit, getters }, { loanid }) {
      const { data } = await ApiService.query("materials", {
        loan: loanid,
      });
      commit("fetchMaterialsSuccess", data);
      return getters.list;
    },
    async fetchMaterialsByIds(
      { commit, getters },
      { gmids, smids } = { gmids: [], smids: [] }
    ) {
      const { data } = await ApiService.query("materials", {
        params: { gmids: gmids.join(), smids: smids.join() },
      });
      commit("fetchMaterialsSuccess", data);
      return getters.list;
    },
    async fetchSingleGenericMaterial(_, { id }) {
      const { data } = await ApiService.get("materials/g", id);
      return data;
    },
    async fetchSingleSpecificMaterial(_, { id }) {
      const { data } = await ApiService.get("materials/s", id);
      return data;
    },
  },

  mutations: {
    fetchMaterialsSuccess(state, data) {
      let genmat = {};
      data.results.generic_materials.forEach((m) => {
        genmat[m["id"].toString()] = m;
      });
      state.genericmaterials = genmat;
      let spemat = {};
      data.results.specific_materials.forEach((m) => {
        spemat[m["id"].toString()] = m;
      });
      state.specificmaterials = spemat;
      state.count = data.count;
    },
    clearMaterials(state){
      state.genericmaterials = {};
      state.specificmaterials = {};
      state.count = 0;
    }
  },
};
