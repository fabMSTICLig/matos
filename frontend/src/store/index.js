import Vue from "vue";
import Vuex from "vuex";
import actions from "./actions";
import mutations from "./mutations";
import getters from "./getters";
import state from "./state";
import auth from "./auth.module";
import organizations from "./organizations.module";
import users from "./users.module";
import families from "./families.module";
import equipments from "./equipments.module";
import affiliations from "./affiliations.module";

Vue.use(Vuex)

export default new Vuex.Store({
  namespaced: true, // namespaced instead namespace
  modules: {
    auth,
    organizations,
    affiliations,
    users,
    families,
    equipments
  }
})
