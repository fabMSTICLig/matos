import Vue from "vue";
import Vuex from "vuex";


import breadcumb from "./breadcumb.module";
import auth from "./auth.module";
import affiliations from "./affiliations.module";
import users from "./users.module";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    breadcumb,
    auth,
    affiliations,
    users,
  }
});
