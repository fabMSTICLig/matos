import createCrud from "./crud.factory";
import ApiService from "../common/api.service";

const loans_extra = {
  state: {
    pendingLoan: null,
    status: {},
  },
  getters: {
    pendingLoan(state) {
      return state.pendingLoan;
    },
    status(state) {
      return state.status;
    },
  },
  actions: {
    async fetchStatus({ commit }) {
      const { data } = await ApiService.query("loans/status");
      commit("setStatus", data);
      return data;
    },
    async makeChild({ commit }, { id }) {
      const { data } = await ApiService.post("loans/" + id + "/make_child");
      commit("updateSuccess", data.parent);
      commit("createSuccess", data.child);
      return data.child;
    },
    async onLoad({ commit, state, dispatch }, id) {
      if (id) commit("setPending", await dispatch("fetchSingle", { id: id }));
      else if (localStorage.getItem("pendingLoan") != null) {
        let loan = JSON.parse(localStorage.getItem("pendingLoan"));
        if (loan.id)
          commit("setPending", await dispatch("fetchSingle", { id: loan.id }));
        else
          commit("setPending", loan);
      } else {
        commit("resetPending");
      }
    },
    copyPending({ commit, state }, data) {
      commit("setPending", Object.assign({}, data, { id: null, status: 3 }));
    },
    addMaterial({ commit, state }, mat) {
      let loan = Object.assign({}, state.pendingLoan);
      if (loan.entity == null) {
        loan.entity = mat.entity;
      }
      if (loan.entity && loan.entity == mat.entity) {
        if ("quantity" in mat) {
          let gen_mat_items = loan.generic_materials;
          let gen_mat_included = gen_mat_items.find((item) => {
            return item.material == mat.id;
          });

          if (gen_mat_included) {
            gen_mat_included.quantity = gen_mat_included.quantity + 1;
          } else {
            loan.generic_materials.push({
              material: mat.id,
              quantity: 1,
            });
          }
        } else if (!(mat.id in loan.specific_materials)) {
          loan.specific_materials[mat.id] = [];
        }
      }
      commit("setPending", loan);
    },
    removeMaterial({ commit, state }, mat) {
      let loan = Object.assign({}, state.pendingLoan);
      if ("quantity" in mat) {
        loan.generic_materials = loan.generic_materials.filter(
          (item) => item.material != mat.id
        );
      } else if (mat.id in loan.specific_materials) {
        delete loan.specific_materials[mat.id];
      }
      if (
        loan.status == null &&
        Object.keys(loan.specific_materials).length == 0 &&
        loan.generic_materials.length == 0
      ) {
        loan.entity = null;
      }
      commit("setPending", loan);
    },
    cleanMaterials({ commit, state }) {
      let loan = Object.assign({}, state.pendingLoan);
      loan.generic_materials = [];
      loan.specific_materials = {};
      if (loan.status == null) {
        loan.entity = null;
      }
      commit("setPending", loan);
    },
  },
  mutations: {
    setStatus(state, status) {
      state.status = status;
    },
    savePending(state) {
      localStorage.setItem("pendingLoan", JSON.stringify(state.pendingLoan));
    },
    setPending(state, data) {
      if (data) {
        state.pendingLoan = data;
      }
      localStorage.setItem("pendingLoan", JSON.stringify(state.pendingLoan));
    },
    resetPending(state) {
      state.pendingLoan = {
        entity: null,
        affiliation: null,
        status: 2,
        user: null,
        due_date: null,
        return_date: null,
        checkout_date: null,
        comments: null,
        specific_materials: {},
        generic_materials: [],
      };
      localStorage.setItem("pendingLoan", JSON.stringify(state.pendingLoan));
    },
  },
};
const loans = createCrud("loans", loans_extra);
export default loans;
