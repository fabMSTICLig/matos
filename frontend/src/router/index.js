import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

function requireAuth(to, from, next) {
    if (store.getters.isAuthenticated) {
        if (to.name == 'profile' || store.getters.authUser.first_name && store.getters.authUser.last_name && store.getters.authUser.email) {
            next()
        } else {
            next({
                name: "profile"
            })
        }
    } else {
        next('/')
    }
}

function requireAdmin(to, from, next) {
    if (store.getters.isAuthenticated && store.getters.isAdmin) {
        next()
    } else {
        next({
            name: "home"
        })
    }
}
const routes = [{
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/about",
        name: "About",
        component: () =>
            import ( /* webpackChunkName: "about" */ "../views/About.vue")
    },
    {
        path: "/profile",
        name: "Profile",
        component: () =>
            import ( /* webpackChunkName: "profile" */ "../views/Profile.vue")
    },
    {
        path: "/affiliations",
        component: () =>
            import (/* webpackChunkName: "affiliation" */ "../views/Affiliations.vue"),
        beforeEnter: requireAdmin,
        children :[
            {
                path: "",
                name: "affiliations",
                component: () =>
                    import (/* webpackChunkName: "affiliationlist" */"../views/AffiliationsList.vue"),
            },
            {
                path: ":id",
                name : "affiliation",
                component: () =>
                    import (/* webpackChunkName: "affiliationedit" */ "../views/AffiliationEdit.vue"),
            },
        ],
    },

];

const router = new VueRouter({
    routes
});

export default router;
