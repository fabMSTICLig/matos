import { createApp } from "vue";
import { createPinia } from "pinia";
// import "bootstrap/dist/css/bootstrap.min.css";
import "../src/assets/CSS/bootstrap_UGA-graphic.css";

import Modal from "./plugins/modal";

import App from "./App.vue";
import router from "./route";
import { useAuthStore } from "./stores/auth";
import ApiService from "./helpers/api.service";

ApiService.init();

const app = createApp(App);
var pinia = createPinia();
app.use(pinia);
app.use(router)
app.use(Modal);

const authStore = useAuthStore()

app.config.globalProperties.$filters = {
  field(value, fieldname) {
    if (value) return value[fieldname];
    else return "";
  },
};

authStore.checkAuth().finally(() => {
  app.mount("#app");
});
