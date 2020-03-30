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
import { CHECK_AUTH } from './store/actions.type'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
ApiService.init()

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  Promise.all([store.dispatch(CHECK_AUTH)])
    .then(next)
    .catch(next)
})

Vue.config.devtools = true
sync(store, router)

new Vue({
  router,
  store,
  sync,
  render: h => h(App)
}).$mount('#app')
