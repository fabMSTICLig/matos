<template>
    <div id="app">
        <div id="header">
          <div class="nav-header">
            <router-link tag="a" class="button-head" class-active="active" to="/" exact>Réservations</router-link>
            <router-link tag="a" class="button-head" class-active="active" to="/manage" exact>Gestion</router-link>
          </div>
          <div class="nav-header">
            <div v-if="!authuser.user">
              <a href="/api/login"  class="button-head-sub">login CAS</a>
            </div>
             <div v-if="authuser.user">
              <a href="/api/self"  class="button-head-sub">{{authuser.user.username}}</a>
            </div>
            <div>
              <a href="/auth/register" class="button-head-sub">Register</a>
            </div>
          </div>
        </div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'App',
  data () {
    return {
      logged: false
    }
  },
  mounted () {
    this.$store.dispatch('getUserInstance')
  },
  computed: {

    ...mapState({
      authuser: state => state.authUser
    })

  }
}
</script>

<style>
@import './assets/css/header.css';
@import './assets/css/bootstrap/bootstrap.min.css';
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
