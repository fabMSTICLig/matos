import { createRouter, createWebHashHistory , RouterView} from "vue-router";
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
    path: "/datapolicy",
    name: "datapolicy",
    component: () => import("../pages/DataPolicy.vue"),
  },
  {
    path: "/legalnotice",
    name: "legalnotice",
    component: () => import("../pages/LegalNotice.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/MyProfile.vue"),
  },
  {
    path: "/loans",
    name: "authloans",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/LoansList.vue"),
  },
  {
    path: "/myloan/:loanid",
    name: "authloan",
    beforeEnter: requireAuth,
    component: () => import("../pages/LoanEdit.vue"),
    props: true,
  },
  {
    path: "/loan/:loanid",
    name: "loan",
    beforeEnter: requireAuth,
    component: () => import("../pages/LoanEdit.vue"),
    props: true,
  },
  {
    path: "/basket",
    name: "basket",
    beforeEnter: requireAuth,
    component: () => import("../pages/LoanEdit.vue"),
  },
  {
    path: "/search",
    name: "search",
    beforeEnter: requireAuth,
    component: () => import("../pages/SearchView.vue"),
  },
  {
    path: "/addmaterial",
    name: "addmaterial",
    beforeEnter: requireAuth,
    component: () => import("../pages/SearchView.vue"),
  },
  {
    path: "/materials/g/:matid",
    component: () => import("../pages/materials/MaterialShow.vue"),
    name: "genericmaterialitem",
    meta: {
      routeparam: "matid",
    },
  },
  {
    path: "/materials/s/:matid",
    component: () => import("../pages/materials/MaterialShow.vue"),
    name: "specificmaterialitem",
    meta: {
      routeparam: "matid",
    },
  },
  {
    path: "/affiliations",
    component: RouterView,
    beforeEnter: requireAdmin,
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
        },
        component: () =>
          import("../pages/admin/affiliations/AffiliationEdit.vue"),
      },
    ],
  },
  {
    path: "/tags",
    component: RouterView,
    beforeEnter: requireAdmin,
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
        },
        component: () => import("../pages/admin/tags/TagEdit.vue"),
      },
    ],
  },
  {
    path: "/users",
    component: RouterView,
    beforeEnter: requireAdmin,
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
        },
        component: () => import("../pages/admin/users/UserEdit.vue"),
      },
    ],
  },
  {
    path: "/showentities",
    name: "showentities",
    beforeEnter: requireAuth,
    component: () => import("../pages/entities/ShowEntities.vue"),
  },
  ...entitiesRoutes,
];
const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
  scrollBehavior () {
    window.scrollTo(0,0);
  }
});

export default router;
