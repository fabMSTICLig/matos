import createCrud from "@/common/storeCrudHelper";
import ApiService from "@/common/api.service";
import { SET_MATERIAL_LOANS } from "./mutations.type";

const instances_extra = {
  state: {
    loans: {}
  },
  getters: {
    loans(state) {
      return state.loans;
    }
  },
  actions: {
    materialLoans({ commit }, { id_entity, id_specificmaterial, id_instance }) {
      return ApiService.query(
        "entities/" +
          id_entity +
          "/specificmaterials/" +
          id_specificmaterial +
          "/instances/" +
          id_instance +
          "/loans",
        {}
      )
        .then(({ data }) => {
          commit(SET_MATERIAL_LOANS, data);
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mutations: {
    setMaterialLoans(state, loans) {
      state.loans = loans;
    }
  }
};
const instances = createCrud("instances", instances_extra);

const specific_extra = {
  modules: {
    instances: instances
  }
};
const specific = createCrud("specificmaterials", specific_extra);

const generic_extra = {
  namespace: true,
  state: {
    loans: {}
  },
  getters: {
    loans(state) {
      return state.loans;
    }
  },
  actions: {
    getLoans({ commit }, { id_entity, id_genericmaterial }) {
      return ApiService.query(
        "entities/" +
          id_entity +
          "/genericmaterials/" +
          id_genericmaterial +
          "/loans",
        {}
      )
        .then(({ data }) => {
          commit(SET_MATERIAL_LOANS, data);
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mutations: {
    setMaterialLoans(state, loans) {
      state.loans = loans;
    }
  }
};
const generic = createCrud("genericmaterials", generic_extra);
const entities_extra = {
  modules: {
    genericMaterials: generic,
    specificMaterials: specific
  }
};
const entities = createCrud("entities", entities_extra);
export default entities;
