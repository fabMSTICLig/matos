<template>
  <div class="container-fluid">
    <div v-if="loaded">
      <Header />
      <router-view class="mr-5 ml-5" />
      <Footer />
    </div>
    <modal
      id="modal-cookie"
      title="Utilisation de cookie"
      :show="showCookie"
      hide-footer
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

<script setup>
import { useStore } from "vuex";
import Modal from "@/plugins/modal";
import Header from "@/components/AppHeader.vue";
import Footer from "@/components/AppFooter.vue";

import { ref, onMounted } from "vue";

const loaded = ref(false);
const showCookie = ref(false);
const store = useStore();
onMounted(async () => {
  document.title = import.meta.env.VITE_APP_TITLE;
  try {
    if (store.getters.isAuthenticated) {
      await store.dispatch("checkAuth");
    }
    console.log("connected");
    const affiliationsPromise = import("./store/affiliations.module");
    const tagsPromise = import("./store/tags.module");
    const usersPromise = import("./store/users.module");
    const entitiesPromise = import("./store/entities.module");
    const loansPromise = import("./store/loans.module");
    const materialsPromise = import("./store/materials.module");

    const affiliations = await affiliationsPromise;
    const tags = await tagsPromise;
    const users = await usersPromise;
    const entities = await entitiesPromise;
    const loans = await loansPromise;
    const materials = await materialsPromise;

    store.registerModule("affiliations", affiliations.default);
    store.registerModule("tags", tags.default);
    store.registerModule("users", users.default);
    store.registerModule("entities", entities.default);
    store.registerModule("loans", loans.default);

    store.registerModule("genericmaterials", materials.genericmaterials);
    store.registerModule("specificmaterials", materials.specificmaterials);
    store.registerModule("materials", materials.materials);

    await store.dispatch("loans/onLoad");
  } catch (e) {
    console.log(e);
  } finally {
    loaded.value = true;
  }

  if (localStorage.getItem("cookiepopup") == null) {
    showCookie.value = true;
  }
});
function validCookie() {
  localStorage.setItem("cookiepopup", "true");
  showCookie.value = false;
}
</script>
