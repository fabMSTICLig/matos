import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
import getters from './getters'
import state from "./state";

    Vue.use(Vuex);

    export default new Vuex.Store({
        namespaced: true, // namespaced instead namespace
        state,
        mutations,
        getters,
        actions
    })