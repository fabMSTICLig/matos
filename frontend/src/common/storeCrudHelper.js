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
        return id => state.entities[id.toString()];
      }
    },
    actions: {
      fetchList({ commit, state, getters }, force = false) {
        if (state.list.length == 0 || force) {
          return ApiService.query(ressource, {})
            .then(({ data }) => {
              commit("fetchListSuccess", data);
              return getters.list;
            })
            .catch(error => {
              Promise.reject(error);
            });
        } else {
          return Promise.resolve(getters.list);
        }
      },
      fetchSingle({ commit }, id) {
        return ApiService.get(ressource, id)
          .then(({ data }) => {
            commit("fetchSingleSuccess", data);
            return data;
          })
          .catch(error => {
            Promise.reject(error);
          });
      },
      create({ commit }, data) {
        return ApiService.post(ressource, data)
          .then(({ data }) => {
            commit("createSuccess", data);
            return data;
          })
          .catch(error => {
            Promise.reject(error);
          });
      },
      update({ commit }, { id, data }) {
        return ApiService.update(ressource, id, data)
          .then(({ data }) => {
            commit("updateSuccess", data);
            return data;
          })
          .catch(error => {
            Promise.reject(error);
          });
      },
      destroy({ commit }, id) {
        console.log(id);
        return ApiService.delete(ressource, id)
          .then(({ data }) => {
            commit("destroySuccess", id);
            return data;
          })
          .catch(error => {
            Promise.reject(error);
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
