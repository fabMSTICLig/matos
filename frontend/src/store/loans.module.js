import createCrud from "@/common/storeCrudHelper";
import ApiService from "@/common/api.service";

const loans_extra = {
  state: {
    pending_loan: null,
    status: {}
  },
  getters: {
    pending_loan(state) {
      return state.pending_loan;
    },
    status(state) {
      return state.status;
    }
  },
  actions: {
    fetchStatus({ commit }) {
      return ApiService.query("loans/status", {}).then(({ data }) => {
        commit("setStatus", data);
        return data;
      });
    },
    makeChild({ commit }, { id }) {
      return ApiService.post("loans/" + id + "/make_child").then(({ data }) => {
        console.log(data);
        commit("updateSuccess", data.parent);
        commit("createSuccess", data.child);
        return data.child;
      });
    }
  },
  mutations: {
    setStatus(state, status) {
      state.status = status;
    },
    onLoad(state) {
      if (localStorage.getItem("pending_loan") != null) {
        var loan = JSON.parse(localStorage.getItem("pending_loan"));
        state.pending_loan = loan;
      } else {
        state.pending_loan = {
          entity: null,
          status: 1,
          user: null,
          due_date: null,
          return_date: null,
          checkout_date: null,
          comments: null,
          specific_materials: [],
          models: [],
          generic_materials: []
        };
        localStorage.setItem(
          "pending_loan",
          JSON.stringify(state.pending_loan)
        );
      }
    },
    setPending(state, data) {
      if (data) {
        state.pending_loan = data;
        localStorage.setItem(
          "pending_loan",
          JSON.stringify(state.pending_loan)
        );
      }
    },
    resetPending(state) {
      state.pending_loan = {
        entity: null,
        status: 1,
        user: null,
        due_date: null,
        return_date: null,
        checkout_date: null,
        comments: null,
        specific_materials: [],
        models: [],
        generic_materials: []
      };
      localStorage.setItem("pending_loan", JSON.stringify(state.pending_loan));
    },
    addMaterial(state, mat) {
      if (state.pending_loan.entity == null) {
        state.pending_loan.entity = mat.entity;
      }
      if (
        "quantity" in mat &&
        state.pending_loan.generic_materials.indexOf(mat.id) == -1
      ) {
        state.pending_loan.generic_materials.push({
          material: mat.id,
          quantity: 1
        });
      } else if (state.pending_loan.models.indexOf(mat.id) == -1) {
        state.pending_loan.models.push(mat.id);
      }
      localStorage.setItem("pending_loan", JSON.stringify(state.pending_loan));
    },
    removeMaterial(state, mat) {
      if ("quantity" in mat) {
        state.pending_loan.generic_materials = state.pending_loan.generic_materials.filter(
          item => item.material != mat.id
        );
      } else if (state.pending_loan.models.indexOf(mat.id) > -1) {
        state.pending_loan.models.splice(
          state.pending_loan.models.indexOf(mat.id),
          1
        );
        state.pending_loan.specific_materials = state.pending_loan.specific_materials.filter(
          instance => !mat.instances.includes(instance)
        );
      }
      if (
        state.pending_loan.status == 1 &&
        state.pending_loan.specific_materials.length == 0 &&
        state.pending_loan.generic_materials.length == 0
      ) {
        state.pending_loan.entity = null;
      }
      localStorage.setItem("pending_loan", JSON.stringify(state.pending_loan));
    },
    cleanMaterials(state) {
      state.pending_loan.generic_materials = [];
      state.pending_loan.specific_materials = [];
      state.pending_loan.models = [];
      if (state.pending_loan.status == 1) {
        state.pending_loan.entity = null;
      }
      localStorage.setItem("pending_loan", JSON.stringify(state.pending_loan));
    },
    savePending(state) {
      localStorage.setItem("pending_loan", JSON.stringify(state.pending_loan));
    }
  }
};
const loans = createCrud("loans", loans_extra);
export default loans;
