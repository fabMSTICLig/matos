import Vue from "vue";
import Vuex from "vuex";

import auth from "./auth.module";
import affiliations from "./affiliations.module";
import tags from "./tags.module";
import users from "./users.module";
import entities from "./entities.module";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    affiliations,
    tags,
    users,
    entities
  }
});
