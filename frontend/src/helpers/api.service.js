import axios from "axios";

/*
Définition de l'ApiService
*/
const ApiService = {
  init() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";
  },

  async query(resource, params) {
    return axios.get(resource + "/", { params });
  },

  async get(resource, slug = "") {
    return axios.get(`${resource}/${slug}`);
  },

  async post(resource, data, params) {
    return axios.post(resource + "/", data, {params});
  },

  async update(resource, slug, data, params) {
    return axios.patch(`${resource}/${slug}/`, data,  {params});
  },

  async put(resource, data, params) {
    return axios.put(resource + "/", data, {params});
  },

  async delete(resource, slug = "") {
    return axios.delete(resource + "/" + (slug == "" ? "" : slug + "/"));
  },
};

export default ApiService;
