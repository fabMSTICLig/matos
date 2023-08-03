<template>
  <header id="header" class="header" role="banner">
    <div class="section clearfix">
      <div class="menu_top d-none d-lg-block">
        <div class="container-liquid">
          <div class="row">
            <div class="col-3 col-md-3 col-lg-4 col-xl-6">
              <a
                href="https://www.univ-grenoble-alpes.fr"
                title="Université Grenoble Alpes"
                role="button"
                class="btn btn-back"
              >
                <span class="icon icon-fleche-precedent"> </span>
                <span class="btn-label">Université Grenoble Alpes</span>
              </a>
            </div>
            <div class="col-9 col-md-9 col-lg-8 col-xl-6">
              <div class="float-end">
                <Dropdown
                  v-if="isAuthenticated"
                  :items="userroutes"
                  :label="authUser.username"
                />
                <a v-if="cas" class="btn btn-primary" href="/cas/login">
                  <svg class="svg-icon">
                    <use href="#profile" />
                  </svg>
                  Login</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        class="social-side-menu-wrapper position-fixed h-100 d-none d-lg-flex align-items-center"
      ></div>
      <div id="block-uga-theme-branding">
        <div class="container-liquid">
          <div class="row h-100 position-relative">
            <div class="col-6 col-md-5 col-lg-3 main-logo">
              <a href="/" rel="home" class="site-logo">
                <img :src="`${publicPath}brand.svg`" alt="Accueil" />
              </a>
            </div>
            <div class="site-name-wrapper col-6 col-md-7 col-lg-5">
              <p class="site-name">{{ title }}</p>
              <p class="site-slogan w-100"></p>
            </div>
            <div
              class="col-md-2 d-none logo-entity d-lg-flex justify-content-center"
            ></div>
            <div
              class="col-md-2 d-none d-lg-flex header-search-block justify-content-end align-items-center"
            ></div>
          </div>
        </div>
      </div>
      <nav
        id="block-uga-theme-menu-main"
        class="uga-theme-main-nav navbar navbar-expand-lg"
        role="navigation"
        aria-labelledby="block-uga-theme-menu-main-menu"
      >
        <h2 id="block-uga-theme-menu-main-menu" class="visually-hidden">
          Navigation principale
        </h2>

        <div id="mainMenu" class="container-liquid">
          <div
            id="navbarMainContent"
            class="w-100 d-none d-lg-flex collapse"
            style=""
          >
            <ul class="nav navbar-nav">
              <li v-if="!isAuthenticated" class="nav-item">
                <router-link
                  active-class="active"
                  class="nav-link"
                  exact
                  :to="{ name: 'home' }"
                >
                  Matos
                </router-link>
              </li>

              <li v-if="isAuthenticated" class="nav-item">
                <router-link
                  active-class="active"
                  class="nav-link"
                  exact
                  :to="{ name: 'search' }"
                >
                  Emprunt Matériels
                </router-link>
              </li>

              <li v-if="isAuthenticated" class="nav-item" role="presentation">
                <router-link
                  active-class="active"
                  class="nav-link"
                  exact
                  :to="{ name: 'showentities' }"
                >
                  Liste Entités
                </router-link>
              </li>
              <Dropdown
                v-if="isManager && myEntities.length > 1"
                :items="myEntities"
                label="Gestion entités"
                class="nav-item drop-align-rect"
                is-nav
              />
              <router-link
                v-if="isManager && myEntities.length == 1"
                class="nav-link"
                :to="myEntities[0].to"
                active-class="active"
                exact
              >
                Gestion {{ myEntities[0].label }}
              </router-link>

              <Dropdown
                v-if="isAdmin"
                :items="adminroutes"
                label="Admin"
                class="nav-item"
                is-nav
              />
              <li v-if="isAuthenticated" class="nav-item" role="presentation">
                <router-link
                  v-if="isAuthenticated"
                  class="nav-link"
                  active-class="active"
                  exact
                  :to="{ name: 'basket' }"
                >
                  <svg class="svg-icon">
                    <use href="#basket" />
                  </svg>
                  Panier ({{ loanQuantity }})
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <nav
        id="block-uga-theme-menu-main-mobile"
        class="uga-theme-main-nav navbar navbar-expand-lg"
        role="navigation"
        aria-labelledby="block-uga-theme-menu-main-mobile-menu"
      >
        <h2 id="block-uga-theme-menu-main-mobile-menu" class="visually-hidden">
          Navigation principale mobile
        </h2>

        <div id="mainMenu" class="w-100">
          <div class="navbar-group">
            <div class="container-liquid">
              <div class="col d-flex d-lg-none align-items-stretch">
                <label
                  for="navbar-toggle-menu"
                  class="btn btn-primary navbar-toggler"
                  data-toggle="collapse"
                  data-target="#navbar"
                  aria-expanded="false"
                  aria-controls="navbar"
                  :class="{ collapsed: !menuCollapse }"
                >
                  <span class="icon">
                    <span class="navbar-toggler-icon"></span>
                    <span class="navbar-toggler-icon"></span>
                    <span class="navbar-toggler-icon"></span>
                  </span>
                  <span class="btn-label"> Menu </span>
                </label>
                <a
                  v-if="!isAuthenticated"
                  class="btn btn-primary collapsed"
                  href="/cas/login"
                >
                  <svg class="svg-icon">
                    <use href="#profile" />
                  </svg>
                  <span class="btn-label">Login</span></a
                >
                <router-link
                  v-if="isAuthenticated"
                  class="btn btn-primary collapsed"
                  active-class="active"
                  exact
                  :to="{ name: 'basket' }"
                >
                  <svg class="svg-icon">
                    <use href="#basket" />
                  </svg>
                  <span class="btn-label"> Panier ({{ loanQuantity }}) </span>
                  </router-link>
                  <label
                  for="navbar-toggle-profile"
                  class="btn btn-primary navbar-toggler"
                  data-toggle="collapse"
                  data-target="#navbar"
                  aria-expanded="false"
                  aria-controls="navbar"
                  :class="{ collapsed: !profileCollapse }"
                >
                  <svg class="svg-icon">
                    <use href="#profile" />
                  </svg>
                  <span class="btn-label">Menu utilisateur</span>
                </label>
              </div>
            </div>
          </div>
          <div id="mobileCollapseGroup">
            <input
              id="navbar-toggle-menu"
              v-model="menuCollapse"
              type="checkbox"
              class="d-none"
            />
            <div
              id="navbarMainContent"
              class="navbar-collapse collapse"
              data-bs-parent="#mobileCollapseGroup"
              :class="{ show: menuCollapse }"
            >
              <div class="container-liquid">
                <ul class="nav navbar-nav">
                  <li v-if="!isAuthenticated" class="nav-item">
                    <router-link
                      active-class="active"
                      class="nav-link"
                      exact
                      :to="{ name: 'home' }"
                    >
                      Matos
                    </router-link>
                  </li>
                  <li v-if="isAuthenticated" class="nav-item">
                    <router-link
                      active-class="active"
                      class="nav-link"
                      exact
                      :to="{ name: 'search' }"
                    >
                      Emprunt Matériels
                    </router-link>
                  </li>

                  <li
                    v-if="isAuthenticated"
                    class="nav-item"
                    role="presentation"
                  >
                    <router-link
                      active-class="active"
                      class="nav-link"
                      exact
                      :to="{ name: 'showentities' }"
                    >
                      Liste Entités
                    </router-link>
                  </li>
                  <Dropdown
                    v-if="isManager && myEntities.length > 1"
                    :items="myEntities"
                    label="Gestion entités"
                    class="dropdown show active"
                    is-nav
                    :absolute="false"
                  />
                  <router-link
                    v-if="isManager && myEntities.length == 1"
                    class="nav-link"
                    :to="myEntities[0].to"
                    active-class="active"
                    exact
                  >
                    Gestion {{ myEntities[0].label }}
                  </router-link>
                  <Dropdown
                    v-if="isAdmin"
                    :items="adminroutes"
                    label="Admin"
                    class="dropdown show active"
                    is-nav
                    :absolute="false"
                  />
                </ul>
              </div>
            </div>
            <input
              id="navbar-toggle-profile"
              v-model="profileCollapse"
              type="checkbox"
              class="d-none"
            />
            <div
              id="navbarProfileContent"
              class="collapse navbar-collapse"
              data-bs-parent="#mobileCollapseGroup"
              :class="{ show: profileCollapse }"
            >
              <div
                id="submenuDropdown-profile"
                class="submenuDropdown-block d-flex d-lg-none"
              >
                <div class="container-liquid">
                  <ul class="nav navbar-nav">
                    <li class="nav-item">
                      <router-link
                        active-class="active"
                        class="nav-link"
                        exact
                        :to="{ name: 'profile' }"
                      >
                        Profile
                      </router-link>
                    </li>
                    <li class="nav-item">
                      <router-link
                        active-class="active"
                        class="nav-link"
                        exact
                        :to="{ name: 'authloans' }"
                      >
                        Mes prêts
                      </router-link>
                    </li>
                    <li class="nav-item">
                      <a href="#" class="nav-link" @click.prevent="logout()">
                        Déconnexion
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </div>

    <svg style="display: none" version="2.0">
      <defs>
        <symbol id="profile" viewBox="0 0 20 20">
          <path
            fill="currentColor"
            d="M12.075,10.812c1.358-0.853,2.242-2.507,2.242-4.037c0-2.181-1.795-4.618-4.198-4.618S5.921,4.594,5.921,6.775c0,1.53,0.884,3.185,2.242,4.037c-3.222,0.865-5.6,3.807-5.6,7.298c0,0.23,0.189,0.42,0.42,0.42h14.273c0.23,0,0.42-0.189,0.42-0.42C17.676,14.619,15.297,11.677,12.075,10.812 M6.761,6.775c0-2.162,1.773-3.778,3.358-3.778s3.359,1.616,3.359,3.778c0,2.162-1.774,3.778-3.359,3.778S6.761,8.937,6.761,6.775 M3.415,17.69c0.218-3.51,3.142-6.297,6.704-6.297c3.562,0,6.486,2.787,6.705,6.297H3.415z"
          />
        </symbol>
        <symbol id="basket" viewBox="0 0 20 20">
          <path
            fill="currentColor"
            d="M0 2.5A.5.5 0 0 1 .5 2H2a.5.5 0 0 1 .485.379L2.89 4H14.5a.5.5 0 0 1 .485.621l-1.5 6A.5.5 0 0 1 13 11H4a.5.5 0 0 1-.485-.379L1.61 3H.5a.5.5 0 0 1-.5-.5zM3.14 5l.5 2H5V5H3.14zM6 5v2h2V5H6zm3 0v2h2V5H9zm3 0v2h1.36l.5-2H12zm1.11 3H12v2h.61l.5-2zM11 8H9v2h2V8zM8 8H6v2h2V8zM5 8H3.89l.5 2H5V8zm0 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0zm9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0z"
          />
        </symbol>
      </defs>
    </svg>
  </header>
</template>

<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useLoansStore } from "@/stores/loans";
import { useEntitiesStore } from "@/stores/entities";
import Dropdown from "./ui/DropdownComponent.vue";

const title = import.meta.env.VITE_APP_TITLE;
const cas = import.meta.env.VITE_APP_CASNAME;
const publicPath = import.meta.env.BASE_URL;

const adminroutes = [
  {
    to: { name: "users" },
    label: "Utilisateurs",
  },
  {
    to: { name: "tags" },
    label: "Tags",
  },
  {
    to: { name: "affiliations" },
    label: "Affiliations",
  },
];
const userroutes = [
  {
    to: { name: "profile" },
    label: "Profile",
  },
  {
    to: { name: "authloans" },
    label: "Mes prêts",
  },
  {
    click: () => {
      logout();
    },
    label: "Déconnection",
  },
];

const myEntities = ref([]);

const menuCollapse = ref(false);
const profileCollapse = ref(false);

const store = useAuthStore();
const { isAuthenticated, authUser, isAdmin, isManager } = storeToRefs(store);

function logout() {
  window.location = authUser.value.externe ? "/cas/logout" : "/auth/logout";
}

const loansStore = useLoansStore();
const { basket } = storeToRefs(loansStore);

const entitiesStore = useEntitiesStore();
const { objects } = storeToRefs(entitiesStore);

onBeforeMount(async () => {
  if (store.isAuthenticated) {
    loansStore.initBasket();
    if (isManager.value) {
      await entitiesStore.fetchList({ ids: authUser.value.entities.join(",") });
      let myEnt = [];
      authUser.value.entities.forEach((ent) => {
        myEnt.push({
          label: objects.value[ent].name,
          to: { name: "entityinfos", params: { entityid: ent } },
        });
      });
      myEntities.value = myEnt;
    }
  }
});

const router = useRouter();
router.beforeEach(() => {
  menuCollapse.value = false;
  profileCollapse.value = false;
  return true;
});

const loanQuantity = computed(() => {
  if (basket.value)
    return (
      basket.value.generic_materials.reduce(
        (a, v) => a + parseInt(v.quantity),
        0
      ) + Object.keys(basket.value.specific_materials).length
    );
  else return 0;
});
</script>
