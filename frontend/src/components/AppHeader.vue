<template>
  <header role="banner">
    <div class="section">
      <div class="menu-top d-lg-block">
          <div class="container-fluid">
              <div class="row">
                  <div class="col-3 col-md-3 col-lg-4 col-xl-6">
                      <a id="back-to-uga" class="btn btn-back" href="https://www.univ-grenoble-alpes.fr/" role="button">
                          <span class="icon icon-fleche-precedent"></span>
                          <span class="btn-label">UNIVERSITÉ GRENOBLE ALPES</span>
                      </a>
                  </div>
              </div>
          </div>
      </div>
      <div id="block-uga-theme-branding"> 
          <div class="container-fluid">
              <div class="row h-100 position-relative">
                  <div class="col-4 col-md-4 col-lg-3 logo-area">
                      <a href="/">
                          <img :src="`${publicPath}brand.svg`" class="logo"/>
                      </a>
                  </div>
                  <div class="col-4 col-md-4 col-lg-4 col-xl-4 d-flex">
                      <h1 class="site-name fw-bold"> {{ title }} </h1>
                  </div>
                  <div class="col-4 d-none d-md-flex justify-content-end">
                    <div v-if="isAuthenticated" class="liste-secondaire">
                      <router-link
                            v-if="isAuthenticated"
                            class="btn btn-primary"
                            active-class="active"
                            exact
                            :to="{ name: 'basket' }"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width="16"
                              height="16"
                              fill="currentColor"
                              class="bi bi-cart4"
                              viewBox="0 0 16 16"
                            >
                              <path
                                d="M0 2.5A.5.5 0 0 1 .5 2H2a.5.5 0 0 1 .485.379L2.89 4H14.5a.5.5 0 0 1 .485.621l-1.5 6A.5.5 0 0 1 13 11H4a.5.5 0 0 1-.485-.379L1.61 3H.5a.5.5 0 0 1-.5-.5zM3.14 5l.5 2H5V5H3.14zM6 5v2h2V5H6zm3 0v2h2V5H9zm3 0v2h1.36l.5-2H12zm1.11 3H12v2h.61l.5-2zM11 8H9v2h2V8zM8 8H6v2h2V8zM5 8H3.89l.5 2H5V8zm0 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0zm9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0z"
                              />
                            </svg>
                            Panier ({{ loanQuantity }})
                          </router-link>
                          <Dropdown :items="userroutes" :label="authUser.username"/>
                          <a class="btn btn-primary" href="#" @click.prevent="logout">Logout </a>
                    </div>
                    <div v-else class="liste-secondaire">
                      <a v-if="cas" class="btn btn-primary" href="/cas/login">Login</a>
                      <a v-if="false" class="btn btn-primary" href="/auth/login">Login</a>
                    </div>
                  </div>
              </div>
          </div>
      </div>
      <nav class="uga-theme-main-nav navbar navbar-light navbar-expand-md">
        <div class="container-fluid">
          <button
            data-toggle="collapse"
            class="navbar-toggler"
            data-target="#navcol-1"
            @click="collapse"
          >
            <span class="navbar-toggler-icon"></span>
            <span class="sr-only">Menu</span>
          </button>
          <div v-if="isAuthenticated" class="d-sm-flex d-md-none liste-secondaire">
            <router-link
                  v-if="isAuthenticated"
                  class="btn btn-primary"
                  active-class="active"
                  exact
                  :to="{ name: 'basket' }"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-cart4"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M0 2.5A.5.5 0 0 1 .5 2H2a.5.5 0 0 1 .485.379L2.89 4H14.5a.5.5 0 0 1 .485.621l-1.5 6A.5.5 0 0 1 13 11H4a.5.5 0 0 1-.485-.379L1.61 3H.5a.5.5 0 0 1-.5-.5zM3.14 5l.5 2H5V5H3.14zM6 5v2h2V5H6zm3 0v2h2V5H9zm3 0v2h1.36l.5-2H12zm1.11 3H12v2h.61l.5-2zM11 8H9v2h2V8zM8 8H6v2h2V8zM5 8H3.89l.5 2H5V8zm0 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0zm9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0z"
                    />
                  </svg>
                  Panier ({{ loanQuantity }})
                </router-link>
                <Dropdown :items="userroutes" :label="authUser.username"/>
                <a class="btn btn-primary" href="#" @click.prevent="logout">Logout </a>
          </div>
          <div v-else class="d-sm-flex d-md-none liste-secondaire">
            <a v-if="cas" class="btn btn-primary" href="/cas/login">Login</a>
            <a v-if="false" class="btn btn-primary" href="/auth/login">Login</a>
          </div>
          <div id="navcol-1" :class="collapsed">
            <ul class="nav navbar-nav">
              <li
                v-if="isAuthenticated"
                class="nav-item"
              >
                <router-link
                  active-class="active"
                  class="nav-link fw-sbold"
                  exact
                  :to="{ name: 'search' }"
                >
                  Emprunt Matériels
                </router-link>
              </li>

              <li v-if="isAuthenticated" class="nav-item" role="presentation">
                <router-link
                  active-class="active"
                  class="nav-link fw-sbold"
                  exact
                  :to="{ name: 'showentities' }"
                >
                  Liste Entités
                </router-link>
              </li>
              <li v-if="isManager" class="vr"></li>
              <Dropdown v-if="isManager && myEntities.length > 1 " :items="myEntities" label="Gestion entités" class="nav-item drop-align-rect fw-sbold" is-nav />
              <router-link
                  v-if="isManager && myEntities.length == 1"
                  class="nav-link"
                  :to="myEntities[0].to"
                  active-class="active"
                  exact
                >
                  Gestion {{myEntities[0].label }}
                </router-link>

              <Dropdown v-if="isAdmin" :items="adminroutes" label="Admin" class="nav-item drop-align-rect fw-sbold" is-nav />
            </ul>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useLoansStore } from "@/stores/loans";
import { useEntitiesStore } from "@/stores/entities";
import Dropdown from "./ui/DropdownComponent.vue";

const title = import.meta.env.VITE_APP_TITLE;
const cas = import.meta.env.VITE_APP_CASNAME;
const publicPath = import.meta.env.BASE_URL

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
];

const myEntities = ref([]);

const collapsed = ref("collapse navbar-collapse");
function collapse() {
  /*
    Emulate bootstrap collapse menu
  */
  if (collapsed.value == "collapse navbar-collapse") {
    collapsed.value = "navbar-collapse";
  } else {
    collapsed.value = "collapse navbar-collapse";
  }
}

const store = useAuthStore();
const { isAuthenticated, authUser, isAdmin, isManager } = storeToRefs(store);

function logout() {
  window.location = authUser.value.externe ? "/cas/logout" : "/auth/logout";
}

const loansStore = useLoansStore();
const { basket } = storeToRefs(loansStore);

const entitiesStore = useEntitiesStore();
const { objects } = storeToRefs(entitiesStore);

onBeforeMount(async()=>{
  loansStore.initBasket()
  if(isManager.value)
  {
    await entitiesStore.fetchList({ids:authUser.value.entities.join(",")})
    let myEnt = []
    authUser.value.entities.forEach((ent)=>{
      myEnt.push({ label:objects.value[ent].name,
                      to:{name: "entityinfos", params:{entityid:ent}}})
    })
    myEntities.value=myEnt;
  }
})

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
