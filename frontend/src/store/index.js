import { createStore } from "vuex";

import auth from "./auth.module";

// Create a new store instance.
const store = createStore({
  modules: {
    auth,
  },
});

export default store;
