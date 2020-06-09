<template>
  <div id="app" class="container">
    <Header />
    <router-view />
  </div>
</template>

<script>
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/bootstrap.min.css";
import "./assets/style.css";
import Header from "@/components/Header";

export default {
  name: "App",
  components: {
    Header
  },
  mounted() {
    document.title = process.env.VUE_APP_TITLE;
  },
  beforeCreate(){
    this.$store.commit('loans/onLoad')
  },
};
</script>

<style>
@media only screen and (min-width: 1200px) {
  .container {
    max-width: 1500px;
  }
}
</style>
