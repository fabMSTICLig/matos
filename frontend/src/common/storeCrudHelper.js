import Vue from "vue";
import ApiService from "@/common/api.service";
function mergeDeep(...objects) {
  const isObject = obj => obj && typeof obj === "object";

  return objects.reduce((prev, obj) => {
    Object.keys(obj).forEach(key => {
      const pVal = prev[key];
      const oVal = obj[key];

      if (Array.isArray(pVal) && Array.isArray(oVal)) {
        prev[key] = pVal.concat(...oVal);
      } else if (isObject(pVal) && isObject(oVal)) {
        prev[key] = mergeDeep(pVal, oVal);
      } else {
        prev[key] = oVal;
      }
    });

    return prev;
  }, {});
}

const createCrud = (ressource, source) => {
  const target = {
    namespaced: true,

    state: {
      entities: {},
      list: []
    },
    getters: {
      list(state) {
        return state.list.map(id => state.entities[id.toString()]);
      },
      byId(state) {
        return id => (id ? state.entities[id.toString()] : null);
      }
    },
    actions: {
      fetchList({ commit, getters }, { prefix = "" } = {}) {
        return ApiService.query(prefix + ressource, {})
          .then(({ data }) => {
            commit("fetchListSuccess", data);
            return Promise.resolve(getters.list);
          })
          .catch(error => {
            return Promise.reject(error);
          });
      },
      fetchSingle({ commit }, { id, prefix = "" }) {
        return ApiService.get(prefix + ressource, id)
          .then(({ data }) => {
            commit("fetchSingleSuccess", data);
            return data;
          })
          .catch(error => {
            return Promise.reject(error);
          });
      },
      create({ commit }, { data, prefix = "" }) {
        return ApiService.post(prefix + ressource, data)
          .then(({ data }) => {
            commit("createSuccess", data);
            return data;
          })
          .catch(error => {
            return Promise.reject(error);
          });
      },
      update({ commit }, { id, data, prefix = "" }) {
        return ApiService.update(prefix + ressource, id, data)
          .then(({ data }) => {
            commit("updateSuccess", data);
            return data;
          })
          .catch(error => {
            return Promise.reject(error);
          });
      },
      destroy({ commit }, { id, prefix = "" }) {
        return ApiService.delete(prefix + ressource, id)
          .then(({ data }) => {
            commit("destroySuccess", id);
            return data;
          })
          .catch(error => {
            return Promise.reject(error);
          });
      }
    },

    mutations: {
      fetchListSuccess(state, data) {
        data.forEach(m => {
          Vue.set(state.entities, m["id"].toString(), m);
        });
        state.list = data.map(m => m["id"].toString());
      },
      fetchSingleSuccess(state, data) {
        const id = data["id"].toString();
        Vue.set(state.entities, id, data);
      },
      createSuccess(state, data) {
        if (data) {
          const id = data["id"].toString();
          Vue.set(state.entities, id, data);
          state.list.push(id);
        }
      },
      updateSuccess(state, data) {
        const id = data["id"].toString();
        Vue.set(state.entities, id, data);
        const listIndex = state.list.indexOf(id);
        if (listIndex >= 0) {
          Vue.set(state.list, listIndex, id);
        }
      },
      destroySuccess(state, id) {
        const listIndex = state.list.indexOf(id.toString());
        if (listIndex >= 0) {
          Vue.delete(state.list, listIndex);
        }
        Vue.delete(state.entities, id.toString());
      }
    }
  };
  return mergeDeep(target, source);
};
export default createCrud;
