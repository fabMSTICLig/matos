import createCrud from "@/common/storeCrudHelper";
import ApiService from "@/common/api.service";

import {
  USER_DATA
} from "./actions.type";
import { SET_USERDATA } from "./mutations.type";

const state = {
  userData: {}
};

const getters = {
  userData(state) {
    return state.userData;
  }
};

const users_extra = {
  getters: {},
  mutations: {}
};

const actions = {
  [USER_DATA](context) {
    return new Promise((resolve) => {
      ApiService.query("self/data", {})
        .then(({ data }) => {
          context.commit(SET_USERDATA, data.user);
          resolve();
        })
        .catch(e => {
          console.log(e);
        });
    });
  },
}
const mutations = {
  [SET_USERDATA](state, userData) {
    state.userData = userData;
  }
};
const users = createCrud("users", users_extra);
export default {
  users,
  actions,
  mutations,
  state,
  getters
};
