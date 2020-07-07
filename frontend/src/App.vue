<template>
  <div id="app" class="container">
    <div v-if="loaded">
      <Header />
      <router-view />
      <link rel="stylesheet" href="/static/bootstrap.min.css" />
    </div>
  </div>
</template>

<script>
import "./assets/style.css";
import Header from "@/components/Header";
import { mapGetters } from "vuex";
import { CHECK_AUTH } from "./store/actions.type";

export default {
  name: "App",
  components: {
    Header
  },
  data() {
    return {
      loaded: false
    };
  },
  computed: {
    ...mapGetters(["authUser"])
  },
  mounted() {
    document.title = process.env.VUE_APP_TITLE;
    this.$store
      .dispatch(CHECK_AUTH)
      .then(() => {
        /* eslint-disable-next-line no-console */
        console.log("connected");
        var pall = [];
        pall.push(
          import(
            /* webpackChunkName: "store-affiliations" */ "@/store/affiliations.module"
          ).then(module => {
            this.$store.registerModule("affiliations", module.default);
          })
        );
        pall.push(
          import(
            /* webpackChunkName: "store-tags" */ "@/store/tags.module"
          ).then(module => {
            this.$store.registerModule("tags", module.default);
          })
        );
        pall.push(
          import(
            /* webpackChunkName: "store-users" */ "@/store/users.module"
          ).then(module => {
            this.$store.registerModule("users", module.default);
          })
        );
        pall.push(
          import(
            /* webpackChunkName: "store-entities" */ "@/store/entities.module"
          ).then(module => {
            this.$store.registerModule("entities", module.default);
          })
        );
        pall.push(
          import(
            /* webpackChunkName: "store-loans" */ "@/store/loans.module"
          ).then(module => {
            this.$store.registerModule("loans", module.default);
            this.$store.commit("loans/onLoad");
          })
        );
        pall.push(
          import(
            /* webpackChunkName: "store-materials" */ "@/store/materials.module"
          ).then(module => {
            this.$store.registerModule(
              "genericmaterials",
              module.genericmaterials
            );
            this.$store.registerModule(
              "specificmaterials",
              module.specificmaterials
            );
          })
        );
        Promise.all(pall).then(() => {
          /* eslint-disable-next-line no-console */
          console.log("loaded");
          this.loaded = true;
          /* eslint-disable-next-line no-console */
          console.log(this.loaded);
        });
      })
      .catch(() => {
        this.loaded = true;
      });
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
