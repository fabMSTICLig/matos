import Vue from 'vue'
import VueRouter from 'vue-router'
// import store from './store'
Vue.use(VueRouter)

/** function requireAuthManager (to, from, next) {
  if (store.getters.authUser.is_manager) {
    console.log(store.getters.authUser)
    next()
  } else {
    next({ name: 'home' })
  }
}**/

export default new VueRouter({
  routes: [
    {
      name: 'home',
      path: '/',
      component: () => import('./views/Home')
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
      name: 'entities',
      path: '/entities',
      component: () => import('./views/Entities')
    },
    {
      name: 'entity',
      path: '/entities/:id',
      component: () => import('./views/Entities')
    },
    {
      name: 'entitiesList',
      path: '/entities-list',
      component: () => import('./views/Entities')
    },
    {
      name: 'manageUsers',
      path: '/manage-users',
      component: () => import('./views/ManageUsers')
    }
  ]
})
