import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store'
Vue.use(VueRouter)

function requireAuthAdmin (to, from, next) {
  if (store.getters.authUser.is_staff) {
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
      component: () => import('./views/EntityList')
    },
    {
      name: 'createEntity',
      path: '/entities/create',
      component: () => import('./views/EntityManage'),
      beforeEnter: requireAuthAdmin
    },
    {
      name: 'entity',
      path: '/entities/:id',
      component: () => import('./views/Entities'),
      children: [
        {
          name: 'manageUsers',
          path: '/entities/:id/users',
          component: () => import('./views/ManageUsers'),
          beforeEnter: requireAuthAdmin
        }
      ]
    }
  ]
})
