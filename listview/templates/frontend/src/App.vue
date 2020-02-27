<template>
    <div id="app">
        <div id="header">
          <div class="nav-header">
            <a class="button-head" href="/">
              <span><h4>Réservations</h4></span>
            </a>
          </div>
          <div class="nav-header">
            <a class="button-head"  href="/prets">
              <span><h4 class="headline text-uppercase">Prêts</h4></span>
            </a>
          </div>
          <div class="nav-header">
            <a class="button-head-sub" href="/admin/">Admin</a>
            <div v-if="logged">
              <a class="button-head-sub" href="/logout">Logout</a>
            </div>
          </div>
          <div class="nav-header">
            <div>
              <router-link to="/login" class="button-head-sub">login</router-link>
            </div>
            <div>
              <router-link to="/register" class="button-head-sub">Register</router-link>
            </div>
          </div>
        </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      logged: false
    }
  }
}
</script>

<style>
@import './assets/css/header.css';
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
