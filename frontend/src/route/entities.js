import { requireAuth, requireManager } from "./routeGards";
import {RouterView} from "vue-router";

const routes = [
  {
    path: "/entity/:entityid",
    name: "entity",
    component: () => import("../pages/entities/Entity.vue"),
    beforeEnter: requireAuth,
    meta: {
      routeparam: "entityid",
    },
    children: [
      {
        path: "",
        name: "entityinfos",
        component: () => import("../pages/entities/EntityInfos.vue"),
      },
      {
        path: "edit",
        name: "entityedit",
        beforeEnter: requireManager,
        meta: {
          routeparam: "entityid",
        },
        component: () => import("../pages/entities/EntityEdit.vue"),
      },
      {
        path: "materials/",
        name: "materials",
        beforeEnter: requireManager,
        component: RouterView,
        children: [
          {
            path: "",
            name: "materialslist",
            component: () => import("../pages/materials/MaterialsList.vue"),
          },
          {
            path: "g/:matid",
            name: "genericmaterial",
            component: () =>
              import("../pages/materials/GenericMaterialEdit.vue"),
            meta: {
              routeparam: "matid",
            },
          },
          {
            path: "g/bulk",
            name: "genericmaterialbulk",
            component: () =>
              import("../pages/materials/GenericMaterialBulk.vue"),
            meta: {
              routeparam: "matid",
            },
          },
          {
            path: "s/:matid",
            name: "specificmaterial",
            component: () =>
              import("../pages/materials/SpecificMaterialEdit.vue"),
            meta: {
              routeparam: "matid",
            },
          },
          {
            path: "g/:matid/loans",
            name: "genericmaterialloans",
            component: () => import("../pages/profile/LoansList.vue"),
            meta: {
              routeparam: "matid",
            },
          },
          {
            path: "s/:matid/loans",
            name: "specificmaterialloans",
            component: () => import("../pages/profile/LoansList.vue"),
            meta: {
              routeparam: "matid",
            },
          },
        ],
      },
      {
        path: "loans",
        name: "entityloans",
        beforeEnter: requireManager,
        meta: {
          routeparam: "entityid",
          breadcumb: {
            label: "Prêts",
            name: "entityloans",
          },
        },
        component: () => import("../pages/profile/LoansList.vue"),
      },
      {
        path: "stats",
        name: "entityStats",
        beforeEnter: requireManager,
        meta: {
          routeparam: "entityid",
        },
        component: () => import("../pages/stats/ShowStats.vue"),
      },
    ],
  },
];
export default routes;
