<template>
  <div id="app" class="container">
    <link rel="stylesheet" href="/static/bootstrap.min.css" />
    <div v-if="loaded">
      <Header />
      <router-view />
      <Footer />
    </div>
    <modal
      id="modal-cookie"
      title="Utilisation de cookie"
      v-model="showCookie"
      hideFooter
    >
      <p>
        Ce site utilise des cookies afin de fonctionner. Ils sont uniquement
        utilisés pour gerer la session de l'utilisateur. Il n'y a pas de cookie
        de tierces parties ou d'utilisation à des fins statistiques.
      </p>

      <div>
        <div class="btn-group" role="group" aria-label="Accepter">
          <button type="button" class="btn btn-primary" @click="validCookie">
            J'ai compris
          </button>
        </div>
      </div>
    </modal>
  </div>
</template>

<script>
import "./assets/style.css";
import Modal from "@/components/Modal";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { mapGetters } from "vuex";
import { CHECK_AUTH } from "./store/actions.type";
/*
  Initialisation de l'application
  Cookie déposé à la première utilisation
  Chargement des différents stores
*/
export default {
  name: "App",
  components: {
    Header,
    Footer,
    Modal
  },
  data() {
    return {
      loaded: false,
      showCookie: false
    };
  },
  computed: {
    ...mapGetters(["authUser"])
  },
  methods: {
    validCookie() {
      localStorage.setItem("cookiepopup", "true");
      this.showCookie = false;
    }
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
            this.$store.registerModule("materials", module.materials);
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
    if (localStorage.getItem("cookiepopup") == null) {
      this.showCookie = true;
    }
  }
};
</script>
