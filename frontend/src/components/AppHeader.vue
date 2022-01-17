<template>
  <nav class="navbar navbar-light navbar-expand-md">
    <div class="container-fluid">
      <a
        class="navbar-brand"
        href="/"
      ><strong>{{ title }}</strong></a>
      <button
        data-toggle="collapse"
        class="navbar-toggler"
        data-target="#navcol-1"
        @click="collapse"
      >
        <span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon" />
      </button>
      <div
        id="navcol-1"
        :class="collapsed"
      >
        <ul class="nav navbar-nav me-auto">
          <li
            class="nav-item"
            role="presentation"
          >
            <router-link
              active-class="active"
              class="nav-link"
              exact
              :to="{ name: 'home' }"
            >
              Home
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
              :to="{ name: 'search' }"
            >
              Matériels
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
              :to="{ name: 'entitieslist' }"
            >
              Entités
            </router-link>
          </li>
          <Dropdown
            v-if="isAdmin"
            :items="adminroutes"
            label="Admin"
            is-nav
          />
        </ul>
        <ul
          v-if="isAuthenticated"
          class="nav navbar-nav d-flex"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <router-link
              v-if="isAuthenticated"
              class="nav-link"
              active-class="active"
              exact
              :to="{ name: 'loan' }"
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
              Prêt ({{ loanQuantity }})
            </router-link>
          </li>

          <Dropdown
            :items="userroutes"
            :label="authUser.username"
            is-nav
          />

          <li
            class="nav-item"
            role="presentation"
          >
            <a
              class="nav-link"
              href="#"
              @click.prevent="logout"
            >Logout </a>
          </li>
        </ul>
        <ul
          v-else
          class="nav navbar-nav"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <a
              v-if="cas"
              class="nav-link"
              href="/cas/login"
            >Login</a>
          </li>
          <li
            v-if="false"
            class="nav-item"
            role="presentation"
          >
            <a
              class="nav-link"
              href="/auth/login"
            >Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import Dropdown from "./ui/Dropdown.vue";

const title = import.meta.env.VITE_APP_TITLE;
const cas = import.meta.env.VITE_APP_CASNAME;

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

const store = useStore();
const authUser = computed(() => store.getters.authUser);
const isAuthenticated = computed(() => store.getters.isAuthenticated);
const isAdmin = computed(() => store.getters.isAdmin);

function logout() {
  /*
    TODO: authentication always externe CAS
    logout on auth django in development
  */
  store.commit("loans/resetPending");
  window.location = authUser.value.externe ? "/cas/logout" : "/auth/logout";
}

const loanQuantity = computed(() => {
  return (
    store.getters["loans/pendingLoan"].generic_materials.reduce(
      (a, v) => a + parseInt(v.quantity),
      0
    ) +
    Object.keys(store.getters["loans/pendingLoan"].specific_materials).length
  );
});
</script>
