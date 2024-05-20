<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <header id="header" class="header" role="banner">
    <div class="section clearfix">
      <div class="uga-menu-top navbar bg-white d-none d-lg-block">
        <div class="container-liquid">
          <div class="navbar-nav">
            <a
              href="https://www.univ-grenoble-alpes.fr"
              title="Université Grenoble Alpes"
              role="button"
              class="btn-back nav-link"
            >
              <span class="icon icon-fleche-precedent">&lt; </span>
              <span class="btn-label">Université Grenoble Alpes</span>
            </a>
          </div>
          <div class="navbar-nav">
            <Dropdown
              v-if="isAuthenticated"
              :items="userroutes"
              :label="authUser.username"
              isNav
            >
              <span class="btn-label">{{ authUser.username }}</span>
            </Dropdown>
            <a
              v-if="!isAuthenticated"
              class="btn btn-primary"
              href="/cas/login"
            >
              <svg class="svg-icon">
                <use href="#profile" />
              </svg>
              Login</a
            >
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
        class="uga-theme-main-nav navbar navbar-dark navbar-expand-lg d-none d-lg-block bg-primary"
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
                is-black
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
                is-black
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
        class="uga-theme-main-nav navbar navbar-dark navbar-expand-lg d-block d-lg-none bg-primary"
        role="navigation"
        aria-labelledby="block-uga-theme-menu-main-mobile-menu"
      >
        <h2 id="block-uga-theme-menu-main-mobile-menu" class="visually-hidden">
          Navigation principale mobile
        </h2>
        <div class="container-liquid">
          <label
            for="navbar-toggle-menu"
            class="navbar-toggler btn btn-primary"
            data-toggle="collapse"
            data-target="#navbarMenu"
            aria-expanded="false"
            aria-controls="navbarMenu"
            :class="{ collapsed: !menuCollapse }"
          >
            <svg class="svg-icon">
              <use href="#burger" />
            </svg>
            <span class="btn-label"> Menu </span>
          </label>
          <a
            v-if="!isAuthenticated"
            class="navbar-toggler collapsed btn btn-primary"
            href="/cas/login"
          >
            <svg class="svg-icon">
              <use href="#profile" />
            </svg>
            <span class="btn-label">Login</span></a
          >
          <router-link
            v-if="isAuthenticated"
            class="navbar-toggler collapsed btn btn-primary"
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
            v-if="isAuthenticated"
            for="navbar-toggle-profile"
            class="navbar-toggler btn btn-primary"
            data-toggle="collapse"
            data-target="#navbarProfile"
            aria-expanded="false"
            aria-controls="navbarProfile"
            :class="{ collapsed: !profileCollapse }"
          >
            <svg class="svg-icon">
              <use href="#profile" />
            </svg>
            <span class="btn-label">Menu utilisateur</span>
          </label>
          </div>
          <input
            id="navbar-toggle-menu"
            v-model="menuCollapse"
            type="checkbox"
            class="navbar-toggler-input"
          />
        <div
          id="navbarMainContent"
          class="navbar-collapse collapse ps-4"
          data-bs-parent="#mobileCollapseGroup"
          :class="{ show: menuCollapse }"
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
              class="dropdown show active"
              is-nav
              is-black
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
              is-black
              :absolute="false"
            />
          </ul>
        </div>

          <input
            id="navbar-toggle-profile"
            v-model="profileCollapse"
            type="checkbox"
            class="navbar-toggler-input"
          />
        <div
          id="navbarProfileContent"
          class="collapse navbar-collapse"
          :class="{ show: profileCollapse }"
        >
          <ul class="nav navbar-nav ps-4">
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
      </nav>
    </div>

    <svg style="display: none" version="2.0">
      <defs>
        <symbol id="burger" viewBox="0 0 20 20">
          <path
            fill="currentColor"
            d="M3.314,4.8h13.372c0.41,0,0.743-0.333,0.743-0.743c0-0.41-0.333-0.743-0.743-0.743H3.314
								c-0.41,0-0.743,0.333-0.743,0.743C2.571,4.467,2.904,4.8,3.314,4.8z M16.686,15.2H3.314c-0.41,0-0.743,0.333-0.743,0.743
								s0.333,0.743,0.743,0.743h13.372c0.41,0,0.743-0.333,0.743-0.743S17.096,15.2,16.686,15.2z M16.686,9.257H3.314
								c-0.41,0-0.743,0.333-0.743,0.743s0.333,0.743,0.743,0.743h13.372c0.41,0,0.743-0.333,0.743-0.743S17.096,9.257,16.686,9.257z"
          ></path>
        </symbol>
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
