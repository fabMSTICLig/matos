import createCrud from "./crud.factory";
import ApiService from "../common/api.service";

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
    async fetchTypes({ commit }) {
      const { data } = await ApiService.query("affiliations/types", {});
      commit("setTypes", data);
      return data;
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
