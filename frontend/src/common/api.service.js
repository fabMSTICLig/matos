import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {
    API_URL
} from "@/common/config";



const ApiService = {
    init() {
        Vue.use(VueAxios, axios);
        Vue.axios.defaults.baseURL = API_URL;
        Vue.axios.defaults.timeout = 10000;
        Vue.axios.defaults.headers.common[
            "Content-Type"
        ] = "application/json";
    },

    query(resource, params) {
        return Vue.axios.get(resource, params)
    },

    get(resource, slug = "") {
        return Vue.axios.get(`${resource}/${slug}`)
    },

    post(resource, params) {
        return Vue.axios.post(`${resource}`, params);
    },

    update(resource, slug, params) {
        return Vue.axios.patch(`${resource}/${slug}/`, params);
    },

    put(resource, params) {
        return Vue.axios.put(`${resource}`, params);
    },

    delete(resource, slug = "") {
        return Vue.axios.delete(`${resource}/${slug}`)
    }
};

export default ApiService;









