import axios from "axios"
import Vue from "vue"
import VueAxios from "vue-axios"
const API_URL = "http://localhost:8000";

let actions = {
    createEquipment({commit}, equipment) {
        const instance = axios.create({
            baseURL: 'http://localhost:8000',
            timeout: 1000,
            
          });
        instance.defaults.xsrfHeaderName = 'X-CSRFToken'
        instance.defaults.xsrfCookieName = 'csrftoken'
        instance.defaults.headers["Content-Type"] = "application/json"
        instance.defaults.xsrfHeaderName = 'X-CSRFToken'
        instance.defaults.xsrfCookieName = 'csrftoken'
        instance.post('http://localhost:8000/api/equipments/', equipment, {withCredentials: true})
            .then(res => {
                commit('CREATE_EQUIPMENT', res.data)
            }).catch(err => {
                // eslint-disable-next-line no-console
                console.log(err)
            })
    },

    fetchEquipments({commit}) {

       // Vue.use(VueAxios, axios);

        const instance = axios.create({
            baseURL: 'http://localhost:8000',
            timeout: 1000,
            
          });
        
        instance.defaults.xsrfHeaderName = 'X-CSRFToken'
        instance.defaults.xsrfCookieName = 'csrftoken'
        instance.defaults.headers["Content-Type"] = "application/json"
    
        instance.get('http://localhost:8000/api/equipments/', { headers: {
            }
        }
        )
        .then(res => {
            console.log("Data",JSON.stringify(res, null, 4))
            commit('FETCH_EQUIPMENTS', res.data)
        })
        .catch(err => {
            // eslint-disable-next-line no-console
            console.log(err)
        })

        console.log(axios.defaults.headers);
    },
    deleteEquipment({commit}, equipment) {
        const instance = axios.create({
            baseURL: 'http://localhost:8000',
            timeout: 1000,
            
          });
        
        instance.defaults.xsrfHeaderName = 'X-CSRFToken'
        instance.defaults.xsrfCookieName = 'csrftoken'
        instance.defaults.headers["Content-Type"] = "application/json"

       instance.delete(`http://localhost:8000/equipments/${equipment.id}`)
            .then(res => {
                if (res.data === 'ok')
                    commit('DELETE_EQUIPMENT', equipment)
            }).catch(err => {
            // eslint-disable-next-line no-console
            console.log(err)
        })
    }
}

export default actions