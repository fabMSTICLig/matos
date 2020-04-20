import Vue from 'vue'
import Vuex from 'vuex'
import auth from './auth.module'
import entities from './entities.module'
import users from './users.module'
import families from './families.module'
import equipments from './equipments.module'
import affiliations from './affiliations.module'

Vue.use(Vuex)

export default new Vuex.Store({
  namespaced: true, // namespaced instead namespace
  modules: {
    auth,
    entities,
    affiliations,
    users,
    families,
    equipments
  }
})
