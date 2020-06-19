import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { BootstrapVue, DropdownPlugin } from "bootstrap-vue";
import { CHECK_AUTH } from "./store/actions.type";
import ApiService from "./common/api.service";

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(DropdownPlugin);

Vue.filter("field", function(value, field) {
  if (!value || !(field in value)) return "";
  return value[field];
});

ApiService.init();

router.beforeEach((to, from, next) => {
  Promise.all([store.dispatch(CHECK_AUTH)])
    .then(next)
    .catch(next);
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
