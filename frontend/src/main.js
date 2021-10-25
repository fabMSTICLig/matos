import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { CHECK_AUTH } from "./store/actions.type";
import ApiService from "./common/api.service";
import vueDebounce from "vue-debounce";

// Setting a different event to listen to
Vue.use(vueDebounce, {
  listenTo: "input",
});

Vue.config.productionTip = false;

Vue.filter("field", function (value, field) {
  if (!value || !(field in value)) return "";
  return value[field];
});

Vue.prototype.$removeFromArray = (array, elem) => {
  var index = array.indexOf(elem);
  if (index > -1) {
    array.splice(index, 1);
  }
};

ApiService.init();

router.beforeEach((to, from, next) => {
  Promise.all([store.dispatch(CHECK_AUTH)])
    .then(next)
    .catch(next);
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
