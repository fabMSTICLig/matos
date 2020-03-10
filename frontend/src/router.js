import Vue from "vue";
import VueRouter from "vue-router";
import store from "./store";
import auth from './store/auth.module'
import { CHECK_AUTH } from "@/store/actions.type"
import state from "./store/state";
Vue.use(VueRouter)


function requireAuthManager (to, from, next) {
  if (store.getters.isManager) {
    console.log('auth')
    if (store.getters.isManager && store.getters.userAuth.manager) {
         next()
    } else {
      next({ name: 'home' })
    }
  } else {
    next('/')
  }
}


function requireAuthAdmin (to, from, next) {
  Promise.all([store.dispatch(CHECK_AUTH)])
  .then(res => {
        if (store.state.auth.authUser.is_staff) {
          next()
        }
        else {
          next({ name: 'home' })
        }
      })
  .catch(err => {
    next('/')
  })
  
  }
   


 
export default new VueRouter({
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("./views/Home")
    },
    {
      name: "equipment",
      path: "/equipment",
      component: () => import("./views/EquipmentCreate")
    },
    {
      name: "equipmentEdit",
      path: "/equipment/:id",
      component: () => import("./views/EquipmentEdit")
    },
    {
      name: "login",
      path: "/login",
      component: () => import("./views/Login")
    },
    {
      name: "manage",
      path: "/manage",
      component: () => import("./views/Manage"),
      beforeEnter: requireAuthManager
    },
    {
      name: "manageEntity",
      path: "/manage/entity/:id",
      component: () => import("./views/Manage"),
      beforeEnter: requireAuthManager
    },
    {
      name: "manageUsers",
      path: "/manage/users",
      component: () => import("./views/Manage")
    },
    {
      name: "family",
      path: "/families/:id",
      component: () => import("./views/Categorie")
    },
    {
      name: "manageEquipment-list",
      path: "/manage/entity/:id/equipment-list",
      component: () => import("./views/Manage"),
      beforeEnter: requireAuthManager
    },

    {
      name: "admin-orga",
      path: "/admin/orgas",
      component: () => import("./views/Admin"),
      beforeEnter: requireAuthAdmin
    }
  ]
});
