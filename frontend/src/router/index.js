import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

function requireAuth(to, from, next) {
  if (store.getters.isAuthenticated) {
    if (
      to.name == "profile" ||
      (store.getters.authUser.first_name &&
        store.getters.authUser.last_name &&
        store.getters.authUser.email &&
        store.getters.authUser.rgpd_accept)
    ) {
      next();
    } else {
      next({
        name: "profile"
      });
    }
  } else {
    next("/");
  }
}

function requireAdmin(to, from, next) {
  if (store.getters.isAuthenticated && store.getters.isAdmin) {
    next();
  } else {
    next({
      name: "home"
    });
  }
}
const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/profile",
    name: "profile",
    beforeEnter: requireAuth,
    component: () =>
      import(/* webpackChunkName: "profile" */ "../views/Profile.vue")
  },
  {
    path: "/search",
    name: "search",
    beforeEnter: requireAuth,
    component: () =>
      import(/* webpackChunkName: "search" */ "../views/Search.vue")
  },
  {
    path: "/loan",
    name: "loan",
    beforeEnter: requireAuth,
    component: () => import(/* webpackChunkName: "loan" */ "../views/Loan.vue")
  },
  {
    path: "/loans",
    name: "authloans",
    beforeEnter: requireAuth,
    component: () =>
      import(/* webpackChunkName: "loans" */ "../views/LoansList.vue")
  },
  {
    path: "/affiliations",
    component: () =>
      import(/* webpackChunkName: "affiliation" */ "../views/Affiliations.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Affiliations",
        name: "affiliations"
      }
    },
    children: [
      {
        path: "",
        name: "affiliations",
        component: () =>
          import(
            /* webpackChunkName: "affiliationlist" */ "../views/AffiliationsList.vue"
          )
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
              labelprop: "name"
            },
            name: "affiliation"
          }
        },
        component: () =>
          import(
            /* webpackChunkName: "affiliationedit" */ "../views/AffiliationEdit.vue"
          )
      }
    ]
  },
  {
    path: "/tags",
    component: () => import(/* webpackChunkName: "tag" */ "../views/Tags.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Tags",
        name: "tags"
      }
    },
    children: [
      {
        path: "",
        name: "tags",
        component: () =>
          import(/* webpackChunkName: "taglist" */ "../views/TagsList.vue")
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
              labelprop: "name"
            },
            name: "tag"
          }
        },
        component: () =>
          import(/* webpackChunkName: "tagedit" */ "../views/TagEdit.vue")
      }
    ]
  },
  {
    path: "/users",
    component: () =>
      import(/* webpackChunkName: "user" */ "../views/Users.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Utilisateurs",
        name: "users"
      }
    },
    children: [
      {
        path: "",
        name: "users",
        component: () =>
          import(/* webpackChunkName: "userlist" */ "../views/UsersList.vue")
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
              labelprop: "username"
            },
            name: "user"
          }
        },
        component: () =>
          import(/* webpackChunkName: "useredit" */ "../views/UserEdit.vue")
      }
    ]
  },
  {
    path: "/entities",
    component: () =>
      import(/* webpackChunkName: "entity" */ "../views/Entities.vue"),
    beforeEnter: requireAuth,
    meta: {
      breadcumb: {
        label: "Entités",
        name: "entitieslist"
      }
    },
    children: [
      {
        path: "",
        name: "entitieslist",
        component: () =>
          import(
            /* webpackChunkName: "entitylist" */ "../views/EntitiesList.vue"
          )
      },
      {
        path: ":entityid",
        component: () =>
          import(/* webpackChunkName: "entity" */ "../views/Entity.vue"),
        meta: {
          routeparam: "entityid",
          routedelete: "entities",
          breadcumb: {
            label: {
              ressource: "entities",
              labelprop: "name"
            },
            name: "entityedit"
          }
        },
        children: [
          {
            path: "",
            name: "entityinfos",
            meta: {
              routeparam: "entityid",
              routedelete: "entities"
            },
            component: () =>
              import(
                /* webpackChunkName: "entityedit" */ "../views/EntityInfos.vue"
              )
          },
          {
            path: "/edit",
            name: "entityedit",
            meta: {
              routeparam: "entityid",
              routedelete: "entities"
            },
            component: () =>
              import(
                /* webpackChunkName: "entityedit" */ "../views/EntityEdit.vue"
              )
          },
          {
            path: "materials",
            meta: {
              breadcumb: {
                label: "Materiels",
                name: "materialslist"
              }
            },
            component: () =>
              import(
                /* webpackChunkName: "materials" */ "../views/Materials.vue"
              ),
            children: [
              {
                path: "",
                name: "materialslist",
                component: () =>
                  import(
                    /* webpackChunkName: "materialslist" */ "../views/MaterialsList.vue"
                  )
              },
              {
                path: "g/:matid",
                name: "genericmaterial",
                component: () =>
                  import(
                    /* webpackChunkName: "genmaterial" */ "../views/GenericMaterialEdit.vue"
                  ),
                meta: {
                  routeparam: "matid",
                  routedelete: "materialslist",
                  breadcumb: {
                    label: {
                      ressource: "entities/genericMaterials",
                      prefix: [
                        {
                          ressource: "entities",
                          param: "entityid"
                        }
                      ],
                      labelprop: "name"
                    },
                    name: "genericmaterial"
                  }
                }
              },
              {
                path: "s/:matid",
                name: "specificmaterial",
                component: () =>
                  import(
                    /* webpackChunkName: "spematerial" */ "../views/SpecificMaterialEdit.vue"
                  ),
                meta: {
                  routeparam: "matid",
                  routedelete: "materialslist",
                  breadcumb: {
                    label: {
                      ressource: "entities/specificMaterials",
                      prefix: [
                        {
                          ressource: "entities",
                          param: "entityid"
                        }
                      ],
                      labelprop: "name"
                    },
                    name: "specificmaterial"
                  }
                }
              }
            ]
          },
          {
            path: "loans",
            name: "entityloans",
            meta: {
              routeparam: "entityid",
              breadcumb: {
                label: "Prêts",
                name: "entityloans"
              }
            },
            component: () =>
              import(
                /* webpackChunkName: "entityloanlist" */ "../views/EntityLoansList.vue"
              )
          }
        ]
      }
    ]
  }
];

const router = new VueRouter({
  routes
});

export default router;
