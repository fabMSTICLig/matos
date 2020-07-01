<template>
  <div id="app" class="container">
    <Header />
    <router-view />
    <link rel="stylesheet" href="/static/bootstrap.min.css">
  </div>
</template>

<script>
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
  beforeCreate() {
    this.$store.commit("loans/onLoad");
  }
};
</script>

<style>
@media only screen and (min-width: 1200px) {
  .container {
    max-width: 1500px;
  }
}
</style>
