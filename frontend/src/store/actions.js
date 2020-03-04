import axios from 'axios'

const API_URL = 'http://localhost:8000'

const instance = axios.create({
  baseURL: API_URL,
  timeout: 1000
})
instance.defaults.headers['Content-Type'] = 'application/json'
instance.defaults.xsrfHeaderName = 'X-CSRFToken'
instance.defaults.xsrfCookieName = 'csrftoken'

let actions = {
  createEquipment ({ commit }, equipment) {
    instance
      .post(`${API_URL}/api/equipments/`, equipment, { withCredentials: true })
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

    instance
      .get(`${API_URL}/api/equipments/`, { headers: {} })
      .then(res => {
        commit('FETCH_EQUIPMENTS', res.data)
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.log(err)
      })
  },

  getEquipment ({ commit }, index) {
    instance
      .get(`${API_URL}/api/equipments/${index}`, { headers: {} })
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
    instance
      .get(`${API_URL}/api/families/${index}`, { headers: {} })
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
    instance
      .get(`${API_URL}/api/families/`, { headers: {} })
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
    instance
      .get(`${API_URL}/api/organizations/`, { headers: {} })
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
    instance
      .get(`${API_URL}/api/users/`, { headers: {} })
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
    instance
      .get(`${API_URL}/api/self`, { headers: {} })
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
    instance
      .put(`http://localhost:8000/api/equipments/${equipment.id}/`, equipment, {
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
    instance
      .put(`http://localhost:8000/api/organizations/${entity.id}/`, entity, {
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
   
    instance
      .delete(`http://localhost:8000/equipments/${equipment.id}`)
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
