import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);


export default new VueRouter({
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("./views/Home"),
    },
    {
      name: "equipment",
      path: "/equipment",
      component: () => import("./views/Equipment"),
    },
    {
      name: "equipmentEdit",
      path: "/equipment/:id",
      component: () => import("./views/EquipmentEdit"),
    },
    {
      name: "login",
      path: "/login",
      component: () => import("./views/Login"),
    }
  
    ]

});
