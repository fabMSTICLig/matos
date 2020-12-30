import createCrud from "@/common/storeCrudHelper";

/*
import ApiService from "@/common/api.service";
import { SET_MATERIAL_LOANS, SET_MATERIALS, SET_MATERIAL_AVAILABILITY } from "./mutations.type";

const instances_extra = {
  state: {
    loans: {},
    materials: {}
  },
  getters: {
    loans(state) {
      return state.loans;
    },
    materials(state) {
      return state.materials;
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
          return data;
        })
        .catch(e => {
          console.log(e);
        });
    },
    getMaterials({ commit }, { id }) {
      return ApiService.query("entities/" + id + "/specificmaterials")
        .then(({ data }) => {
          commit(SET_MATERIALS, data);
          return data;
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mutations: {
    setMaterialLoans(state, loans) {
      state.loans = loans;
    },
    setMaterials(state, materials) {
      state.materials = materials;
    }
  }
};
const instances = createCrud("instances", instances_extra);

const specific_extra = {
  modules: {
    instances: instances
  },
  actions: {
    getMaterialAvailability({ commit }, { id_entity, id_model, id_instance, data }) {
        return ApiService.post(
          "entities/" +
            id_entity +
            "/specificmaterials/" +
            id_model +
            "/instances/" +
            id_instance +
            "/availability",
            data
        ).then(({ data }) => {
          commit(SET_MATERIAL_AVAILABILITY, data);
          return data;
        })
        .catch(e => {
          console.log(e);
      })
    }
  },
  mutations: {
    setMaterialAvailability(state, materialAvailability) {
      state.materialAvailability = materialAvailability
    }
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
    },
    materials(state) {
      return state.materials;
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
          return data;
        })
        .catch(e => {
          console.log(e);
        });
    },

    getMaterialAvailability({ commit }, { id_entity, id_mat, data }) {

        return ApiService.post(
          "entities/" +
            id_entity +
            "/genericmaterials/" +
            id_mat +
            "/availability",
          data
        )
        .then(({ data }) => {
          commit(SET_MATERIAL_AVAILABILITY, data);
          return data;
        })
        .catch(e => {
          console.log(e);
        })

    },

    getMaterials({ commit }, { id }) {
      return ApiService.query("entities/" + id + "/genericmaterials")
        .then(({ data }) => {
          commit(SET_MATERIALS, data);
          return data;
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mutations: {
    setMaterialLoans(state, loans) {
      state.loans = loans;
    },
    setMaterials(state, materials) {
      state.materials = materials;
    },
    setMaterialAvailability(state, materialAvailability) {
      state.materialAvailability = materialAvailability
    }
  }
};
const generic = createCrud("genericmaterials", generic_extra);*/
const entities_extra = {
/*  modules: {
    genericMaterials: generic,
    specificMaterials: specific
  }*/
};
const entities = createCrud("entities", entities_extra);
export default entities;
