import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.common'
import { sync } from 'vuex-router-sync'
import store from './store/index'
import ApiService from './common/api.service'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
ApiService.init()

Vue.config.productionTip = false
sync(store, router)




new Vue({
  router,
  store,
  sync,
  render: h => h(App)
}).$mount('#app')
