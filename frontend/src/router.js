import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store'
Vue.use(VueRouter)

function requireAuthManager (to, from, next) {
  if (store.getters.authUser.is_manager) {
    console.log(store.getters.authUser)
    next()
  } else {
    next({ name: 'home' })
  }
}

export default new VueRouter({
  routes: [
    {
      name: 'home',
      path: '/',
      component: () => import('./views/Home')
    },
    {
      name: 'organizationList',
      path: '/organisations/:id',
      component: () => import('./views/Organizations')
    },
    {
      name: 'login',
      path: '/login',
      component: () => import('./views/Login')
    },
    {
      name: 'editProfile',
      path: '/profile',
      component: () => import('./views/Profile')
    },
    {
      name: 'manageEntity',
      path: '/manage/:id',
      component: () => import('./views/Manage'),
      beforeEnter: requireAuthManager
    },

    {
      name: 'manageUsers',
      path: '/manage/:id/users',
      component: () => import('./views/Manage')
    },
    {
      name: 'organisations',
      path: '/organisations',
      component: () => import('./views/Organizations')
    }
  ]
})
