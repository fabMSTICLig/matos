<template>
    <div id='app'>
        <div id='header'>
          <div class='nav-header'>
            <router-link tag='a' class='button-head' class-active='active' to='/' exact>Réservations</router-link>
            <router-link tag='a' class='button-head' class-active='active' to='/manage' exact>Gestion</router-link>
            <router-link tag='a' v-if='isAdmin' class='button-head' class-active='active' to='/admin/orgas' exact>Organisations</router-link>
          </div>
          <div class='nav-header'>
            <div v-if='!isAuthenticated' class='auth-nav'>
              <b-link href='/api/login'  class='button-head-sub'>login CAS</b-link>
            </div>
            <div v-if='isAuthenticated' class='auth-nav'>
              <b-link href='/api/self' class='button-head-sub'>{{authUser.username}}</b-link>
            </div>
            <div v-if='isAuthenticated' class='auth-nav'>
              <b-link :href="authUser.externe ? '/api/logout' : '/auth/logout'" >Log out</b-link>
            </div>
            <div v-if='!isAuthenticated' class='auth-nav'>
              <b-link href='/auth/login' class='button-head-sub'>login</b-link>
            </div>
          </div>
        </div>

    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'App',
  components: {
  },
  data () {
    return {
      logged: false
    }
  },
  beforeMount () {
  },
  computed: {

    ...mapGetters(['authUser', 'isAuthenticated', 'isAdmin'])

  }

}
</script>

<style>
@import './assets/css/main.css';
@import './assets/css/bootstrap/bootstrap.min.css';
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
