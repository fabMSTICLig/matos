<template>
  <div class="auth-page">
    <div class="container page">
      <div class="row">
        <div class="col-md-6 offset-md-3 col-xs-12">
          <h1 class="text-xs-center">Sign in</h1>
          <button v-on:click="login();" class="btn btn-lg btn-primary pull-xs-right">
              Sign in
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'RwvLogin',
  data () {
    return {
      logedin: false
    }
  },
  methods: {
    login () {

    }
  },
  computed: {

  }
}
</script>
