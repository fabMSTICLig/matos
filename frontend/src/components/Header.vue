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
              <a class="nav-link" :href="href" @click="navigate">Search</a>
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
          <b-nav-item-dropdown text="Admin" v-if="isAdmin">
            <b-dropdown-item :to="{ name: 'users' }"
              >Utilisateurs</b-dropdown-item
            >
            <b-dropdown-item :to="{ name: 'affiliations' }"
              >Affiliations</b-dropdown-item
            >
            <b-dropdown-item :to="{ name: 'tags' }">Tags</b-dropdown-item>
          </b-nav-item-dropdown>
        </ul>
        <ul v-if="isAuthenticated" class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <router-link
              v-if="isAuthenticated"
              class="nav-link"
              active-class="active"
              exact
              :to="{ name: 'loan' }"
            >Prêt ({{ loanQuantity}})</router-link>
          </li>
          <li class="nav-item" role="presentation">
            <router-link
              class="nav-link"
              active-class="active"
              exact
              :to="{ name: 'profile' }"
              v-text="authUser.username"
            ></router-link>
          </li>

          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              :href="authUser.externe ? '/cas/logout' : '/auth/logout'"
              >Logout</a
            >
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
export default {
  name: "Header",
  data() {
    return {
      title: process.env.VUE_APP_TITLE,
      cas: process.env.VUE_APP_CASNAME
    };
  },

  computed: {
    ...mapGetters(["authUser", "isAuthenticated", "isAdmin"]),
    ...mapGetters({pending_loan:"loans/pending_loan"}),
    loanQuantity(){
        if(this.pending_loan)
            return this.pending_loan.genericmaterials.length + this.pending_loan.specificmaterials.length
        else return ""
    }
  },
  methods: {}
};
</script>
