import createCrud from "@/common/storeCrudHelper";

import ApiService from "@/common/api.service";

const affiliations_extra = {
  state: {
    types: [],
  },
  getters: {
    types(state) {
      return state.types;
    },
  },
  actions: {
    fetchTypes({ commit }) {
      return ApiService.query("affiliations/types", {}).then(({ data }) => {
        commit("setTypes", data);
        return data;
      });
    },
  },
  mutations: {
    setTypes(state, affiliation_types) {
      state.types = affiliation_types;
    },
  },
};
const affiliations = createCrud("affiliations", affiliations_extra);
export default affiliations;
