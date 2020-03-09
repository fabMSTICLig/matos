import axios from 'axios'
import ApiService from '@/common/api.service'

let actions = {
  createEquipment ({ commit }, equipment) {
    ApiService
      .post(`api/equipments/`, equipment, { withCredentials: true })
      .then(res => {
        commit('CREATE_EQUIPMENT', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  fetchEquipments ({ commit }) {
    // Vue.use(VueAxios, axios);

    ApiService
      .get(`api/equipments`)
      .then(res => {
        commit('FETCH_EQUIPMENTS', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getEquipment ({ commit }, index) {
    ApiService
      .get(`api/equipments/${index}`, { headers: {} })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_EQUIPMENT', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getCategory ({ commit }, index) {
    ApiService
      .get(`api/families/${index}`, { headers: {} })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_CATEGORY', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getCategories ({ commit }, index) {
    ApiService
      .get(`api/families`)
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_CATEGORIES', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getOrganizations ({ commit }, index) {
    ApiService
      .get(`api/organizations`)
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_ORGANIZATIONS', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },
  getUsers ({ commit }, index) {
    ApiService
      .get(`api/users/`, { headers: {} })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_USERS', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getUserInstance ({ commit }, index) {
    ApiService
      .get(`api/self`, '', { withCredentials: true })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('AUTH_USER', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },
  
  updateEquipment ({ commit }, equipment) {
    ApiService
      .put(`api/equipment/${equipment.id}`, equipment, {
        withCredentials: true
      })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('GET_EQUIPMENT', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })

    console.log(axios.defaults.headers)
  },

  updateEntity( {commit}, entity) {
    ApiService
      .put(`api/organizations/${entity.id}/`, entity, {
        withCredentials: true
      })
      .then(res => {
        console.log('Data', JSON.stringify(res, null, 4))
        commit('SET_ORGA', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })

    console.log(axios.defaults.headers)
  },

  deleteEquipment ({ commit }, equipment) {
   
    ApiService
      .delete(`api/equipments/${equipment.id}`)
      .then(res => {
        if (res.data === 'ok') commit('DELETE_EQUIPMENT', equipment)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  }
}

export default actions
