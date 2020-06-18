import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

const ApiService = {
  init() {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = process.env.VUE_APP_API_URL;
    Vue.axios.defaults.withCredentials = true;
    Vue.axios.defaults.xsrfHeaderName = "X-CSRFToken";
    Vue.axios.defaults.xsrfCookieName = "csrftoken";
  },

  query(resource, params) {
    return Vue.axios.get(resource + "/", params);
  },

  get(resource, slug = "") {
    return Vue.axios.get(`${resource}/${slug}/`);
  },

  post(resource, params) {
    return Vue.axios.post(resource + "/", params);
  },

  update(resource, slug, params) {
    return Vue.axios.patch(`${resource}/${slug}/`, params);
  },

  put(resource, params) {
    return Vue.axios.put(resource + "/", params);
  },

  delete(resource, slug = "") {
    return Vue.axios.delete(resource + "/" + (slug == "" ? "" : slug + "/"));
  }
};

export default ApiService;
