<template>
  <nav class="navbar navbar-light navbar-expand-md">
    <div class="container-fluid">
      <a class="navbar-brand" href="/"
        ><strong>{{ title }}</strong></a
      >
      <button
        data-toggle="collapse"
        class="navbar-toggler"
        data-target="#navcol-1"
        @click="collapse"
      >
        <span class="sr-only">Toggle navigation</span
        ><span class="navbar-toggler-icon"></span>
      </button>
      <div :class="collapsed" id="navcol-1">
        <ul class="nav navbar-nav mr-auto">
          <router-link
            active-class="active"
            exact
            :to="{ name: 'home' }"
            v-slot="{ href, route, navigate }"
          >
            <li class="nav-item" role="presentation">
              <a class="nav-link" :href="href" @click="navigate">Home</a>
            </li>
          </router-link>
          <router-link
            v-if="isAuthenticated"
            active-class="active"
            exact
            :to="{ name: 'search' }"
            v-slot="{ href, route, navigate }"
          >
            <li class="nav-item" role="presentation">
              <a class="nav-link" :href="href" @click="navigate">Matériels</a>
            </li>
          </router-link>

          <router-link
            v-if="isAuthenticated"
            active-class="active"
            exact
            :to="{ name: 'entitieslist' }"
            v-slot="{ href, route, navigate }"
          >
            <li class="nav-item" role="presentation">
              <a class="nav-link" :href="href" @click="navigate">Entités</a>
            </li>
          </router-link>
          <li v-if="isAdmin" class="nav-item" role="presentation">
            <Dropdown
              :items="adminroutes"
              label="Admin"
              classtoogle="nav-link"
            />
          </li>
        </ul>
        <ul v-if="isAuthenticated" class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <router-link
              v-if="isAuthenticated"
              class="nav-link"
              active-class="active"
              exact
              :to="{ name: 'loan' }"
              ><svg
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
              Prêt ({{ loanQuantity }})</router-link
            >
          </li>

          <li class="nav-item" role="presentation">
            <Dropdown
              :items="userroutes"
              :label="authUser.username"
              classtoogle="nav-link"
            />
          </li>

          <li class="nav-item" role="presentation">
            <a class="nav-link" href="#" @click="logout">Logout </a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <a class="nav-link" v-if="cas" href="/cas/login">{{ cas }}</a>
          </li>
          <li class="nav-item" role="presentation" v-if="false">
            <a class="nav-link" href="/auth/login">Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";
import Dropdown from "@/components/Dropdown";
export default {
  name: "Header",
  components: {
    Dropdown
  },
  data() {
    return {
      title: process.env.VUE_APP_TITLE,
      cas: process.env.VUE_APP_CASNAME,
      collapsed: "collapse navbar-collapse",
      adminroutes: [
        {
          to: { name: "users" },
          label: "Utilisateurs"
        },
        {
          to: { name: "tags" },
          label: "Tags"
        },
        {
          to: { name: "affiliations" },
          label: "Affiliations"
        }
      ],
      userroutes: [
        {
          to: { name: "profile" },
          label: "Profile"
        },
        {
          to: { name: "authloans" },
          label: "Mes prêts"
        }
      ]
    };
  },

  computed: {
    ...mapGetters(["authUser", "isAuthenticated", "isAdmin"]),
    ...mapGetters({ pending_loan: "loans/pending_loan" }),
    loanQuantity() {
      if (this.pending_loan)
        return (
          this.pending_loan.generic_materials.reduce(
            (a, v) => a + parseInt(v.quantity),
            0
          ) + this.pending_loan.models.length
        );
      else return "";
    }
  },
  methods: {
    logout(e) {
      e.preventDefault();
      /*
        TODO: authentication always externe CAS
        logout on auth django in development
      */
      if (this.pending_loan) {
        this.$store.commit("loans/resetPending");
      }
      window.location = this.authUser.externe ? "/cas/logout" : "/auth/logout";
    },
    collapse() {
      /*
        Emulate bootstrap collapse menu
      */
      if (this.collapsed == "collapse navbar-collapse") {
        this.collapsed = "navbar-collapse";
      } else {
        this.collapsed = "collapse navbar-collapse";
      }
    }
  }
};
</script>
