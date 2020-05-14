import { PUSH_BREADCUMB, POP_BREADCUMB } from "./actions.type";
import { PUSH_BREADCUMB_MUT, POP_BREADCUMB_MUT } from "./mutations.type";

export const state = {
  breadcumb_list: []
};
const getters = {
  breadcumb_list(state) {
    return state.breadcumb_list;
  }
};
export const actions = {
  [PUSH_BREADCUMB](context, infos) {
    context.commit(PUSH_BREADCUMB_MUT, infos);
  },
  [POP_BREADCUMB](context) {
    context.commit(POP_BREADCUMB_MUT);
  }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [PUSH_BREADCUMB](state, infos) {
    state.breadcumb_list.push(infos);
  },
  [POP_BREADCUMB](state) {
    state.breadcumb_list.pop();
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
