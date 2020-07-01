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
      >
        <span class="sr-only">Toggle navigation</span
        ><span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navcol-1">
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
              <a class="nav-link" :href="href" @click="navigate">Rechercher</a>
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
              >Prêt ({{ loanQuantity }})</router-link
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
            <a
              class="nav-link"
              href="#"
              @click="logout"
              >Logout
            </a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <a class="nav-link" v-if="cas" href="/cas/login">{{ cas }}</a>
          </li>
          <li class="nav-item" role="presentation">
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
          this.pending_loan.generic_materials.length +
          this.pending_loan.models.length
        );
      else return "";
    }
  },
  methods: {
    logout(e) {
      e.preventDefault();
      if(this.pending_loan) {
          this.$store.commit(this.ressource + "/resetPending", this.pending_loan)
          window.location = this.authUser.externe ? '/cas/logout' : '/auth/logout'
      }
    }
  }
};
</script>
