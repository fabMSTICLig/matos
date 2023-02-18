import { requireAuth, requireManager } from "./routeGards";

/*
function requireManager(to, from, next) {
  if (store.getters.isAuthenticated) {
    var user = store.getters.authUser;
    if (
      user.entities.indexOf(parseInt(to.params["entityid"])) > -1 ||
      store.getters.isAdmin
    ) {
      next();
    } else {
      next("/");
    }
  }
}
*/
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
        component: () => import("../pages/materials/Materials.vue"),
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
    ],
  },
];
/*children: [
    {
      path: "",
      name: "entitieslist",
      component: () => import("../pages/entities/EntitiesList.vue"),
    },
      component: () => import("../pages/entities/Entity.vue"),
      meta: {
        routeparam: "entityid",
        routedelete: "entities",
        breadcumb: {
          label: {
            ressource: "entities",
            labelprop: "name",
          },
          name: "entityinfos",
        },
      },
      children: [
        {
          path: "",
          name: "entityinfos",
          meta: {
            routeparam: "entityid",
            routedelete: "entities",
          },
          component: () => import("../pages/entities/EntityInfos.vue"),
        },
        {
          path: "edit",
          name: "entityedit",
          beforeEnter: requireManager,
          meta: {
            routeparam: "entityid",
            routedelete: "entities",
            breadcumb: {
              label: "Edit",
              name: "entityedit",
            },
          },
          component: () => import("../pages/entities/EntityEdit.vue"),
        },
        {
          path: "materials",
          beforeEnter: requireManager,
          meta: {
            breadcumb: {
              label: "Materiels",
              name: "materialslist",
            },
          },
          component: () => import("../pages/materials/Materials.vue"),
          children: [
            {
              path: "",
              name: "materialslist",
              component: () => import("../pages/materials/MaterialsList.vue"),
            },
            {
              path: "g/bulk",
              name: "genericmaterialbulk",
              component: () =>
                import("../pages/materials/GenericMaterialBulk.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: "Ajout Massif",
                  name: "genericmaterialbulk",
                },
              },
            },

            {
              path: "g/:matid",
              name: "genericmaterial",
              component: () =>
                import("../pages/materials/GenericMaterialEdit.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: {
                    ressource: "genericmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                  },
                  name: "genericmaterial",
                },
              },
            },
            {
              path: "g/:matid/loans",
              name: "genericmaterialloans",
              component: () => import("../pages/entities/EntityLoansList.vue"),
              meta: {
                routeparam: "matid",
                breadcumb: {
                  label: {
                    ressource: "genericmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                    labelchild: "Prêts",
                  },
                  name: "genericmaterial",
                },
              },
            },
            {
              path: "s/:matid",
              name: "specificmaterial",
              component: () =>
                import("../pages/materials/SpecificMaterialEdit.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: {
                    ressource: "specificmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                  },
                  name: "specificmaterial",
                },
              },
            },
            {
              path: "s/:matid/loans",
              name: "specificmaterialloans",
              component: () => import("../pages/entities/EntityLoansList.vue"),
              meta: {
                routeparam: "matid",
                breadcumb: {
                  label: {
                    ressource: "specificmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                    labelchild: "Prêts",
                  },
                  name: "specificmaterial",
                },
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
          component: () => import("../pages/entities/EntityLoansList.vue"),
        },
      ],
    },
  ],*/
//};
export default routes;
