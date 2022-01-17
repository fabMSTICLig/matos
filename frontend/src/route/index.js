import { createRouter, createWebHashHistory } from "vue-router";
import { requireAdmin, requireAuth } from "./routeGards";
import Home from "../pages/Home.vue";
import entitiesRoutes from "./entities";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/profile",
    name: "profile",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/Profile.vue"),
  },
  {
    path: "/search",
    name: "search",
    beforeEnter: requireAuth,
    component: () => import("../pages/Search.vue"),
  },
  {
    path: "/loan/:loanid?",
    name: "loan",
    beforeEnter: requireAuth,
    component: () => import("../pages/Loan.vue"),
    props: true,
  },
  {
    path: "/loans",
    name: "authloans",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/LoansList.vue"),
  },
  {
    path: "/materials",
    component: () => import("../pages/materials/Materials.vue"),
    name: "materials",
    meta: {
      breadcumb: {
        label: "Materiels",
        name: "materials",
      },
    },
    children: [
      {
        path: "g/:matid",
        component: () => import("../pages/materials/Material.vue"),
        name: "genericmaterialitem",
        meta: {
          routeparam: "matid",
          breadcumb: {
            label: "materiel générique",
            name: "genericmaterialitem",
          },
        },
      },
      {
        path: "s/:matid",
        component: () => import("../pages/materials/Material.vue"),
        name: "specificmaterialitem",
        meta: {
          routeparam: "matid",
          breadcumb: {
            label: "materiel spécifique",
            name: "specificmaterialitem",
          },
        },
      },
    ],
  },
  {
    path: "/affiliations",
    component: () => import("../pages/admin/affiliations/Affiliations.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Affiliations",
        name: "affiliations",
      },
    },
    children: [
      {
        path: "",
        name: "affiliations",
        component: () =>
          import("../pages/admin/affiliations/AffiliationsList.vue"),
      },
      {
        path: ":affid",
        name: "affiliation",
        meta: {
          routeparam: "affid",
          routedelete: "affiliations",
          breadcumb: {
            label: {
              ressource: "affiliations",
              labelprop: "name",
            },
            name: "affiliation",
          },
        },
        component: () =>
          import("../pages/admin/affiliations/AffiliationEdit.vue"),
      },
    ],
  },
  {
    path: "/tags",
    component: () => import("../pages/admin/tags/Tags.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Tags",
        name: "tags",
      },
    },
    children: [
      {
        path: "",
        name: "tags",
        component: () => import("../pages/admin/tags/TagsList.vue"),
      },
      {
        path: ":tagid",
        name: "tag",
        meta: {
          routeparam: "tagid",
          routedelete: "tags",
          breadcumb: {
            label: {
              ressource: "tags",
              labelprop: "name",
            },
            name: "tag",
          },
        },
        component: () => import("../pages/admin/tags/TagEdit.vue"),
      },
    ],
  },
  {
    path: "/users",
    component: () => import("../pages/admin/users/Users.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Utilisateurs",
        name: "users",
      },
    },
    children: [
      {
        path: "",
        name: "users",
        component: () => import("../pages/admin/users/UsersList.vue"),
      },
      {
        path: ":userid",
        name: "user",
        meta: {
          routeparam: "userid",
          routedelete: "users",
          breadcumb: {
            label: {
              ressource: "users",
              labelprop: "username",
            },
            name: "user",
          },
        },
        component: () => import("../pages/admin/users/UserEdit.vue"),
      },
    ],
  },
  entitiesRoutes,
];
const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

export default router;
