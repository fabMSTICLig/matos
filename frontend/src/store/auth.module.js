import ApiService from "@/common/api.service";

import {
  CHECK_AUTH,
  UPDATE_AUTHUSER,
  UPDATE_PASSWORD,
  UPDATE_RGPD
} from "./actions.type";
import { SET_AUTHUSER, PURGE_AUTH } from "./mutations.type";

const state = {
  authUser: {}
};

const getters = {
  authUser(state) {
    return state.authUser;
  },
  isAuthenticated(state) {
    return !!state.authUser.username;
  },
  isAdmin(state) {
    return state.authUser.is_staff;
  }
};

const actions = {
  [CHECK_AUTH](context) {
    return new Promise((resolve, reject) => {
      ApiService.query("self", {})
        .then(({ data }) => {
          context.commit(SET_AUTHUSER, data.user);
          resolve();
        })
        .catch(e => {
          console.log(e);
          context.commit(PURGE_AUTH);
          reject();
        });
    });
  },
  [UPDATE_AUTHUSER](context, user) {
    return ApiService.update("users", user.id, user).then(({ data }) => {
      context.commit(SET_AUTHUSER, data);
      return data;
    });
  },
  [UPDATE_PASSWORD](context, passwords) {
    return ApiService.put(
      `users/${state.authUser.id}/set_password`,
      passwords
    ).then(() => {
      return "Password changed";
    });
  },
  [UPDATE_RGPD](context) {
    return ApiService.post(`self/rgpd`, { accept: true }).then(({ data }) => {
      context.state.authUser.rgpd_accept = data["rgpd_accept"];
      context.commit(SET_AUTHUSER, context.state.authUser);
    });
  }
};

const mutations = {
  [SET_AUTHUSER](state, user) {
    state.authUser = user;
  },
  [PURGE_AUTH](state) {
    state.authUser = {};
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
