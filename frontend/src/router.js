import Vue from "vue";
import VueRouter from "vue-router";
import store from "./store";

Vue.use(VueRouter);

function requireAuthManager (to, from, next) {
  if (store.getters.isAdmin) {
    console.log('auth')
    if (store.getters.isAdmin && store.getters.userAuth.manager) {
         next()
    } else {
      next({ name: 'home' })
    }
  } else {
    next('/')
  }
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
      component: () => import("./views/Equipment")
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
      name: "manage-entity",
      path: "/manage/entity/:id",
      component: () => import("./views/Manage"),
      beforeEnter: requireAuthManager
    },
    {
      name: "manage-users",
      path: "/manage/users",
      component: () => import("./views/Manage")
    }
  ]
});
