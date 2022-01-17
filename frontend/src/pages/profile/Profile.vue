<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <form id="editor-form" class="form">
        <div class="mb-3">
          <label class="form-label" for="username">Username</label
        ><input
            id="username"
            v-model="authUser.username"
            class="form-control"
            type="text"
            readonly
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="firstname">Prénom</label
        ><input
            id="firstname"
            v-model="authUser.first_name"
            class="form-control"
            type="text"
            required
            readonly
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="lastname">Nom</label
        ><input
            id="lastname"
            v-model="authUser.last_name"
            class="form-control"
            type="text"
            required
            readonly
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="email">Email</label
        ><input
            id="email"
            v-model="authUser.email"
            class="form-control"
            type="email"
            required
            readonly
          />
        </div>
        <div class="mb-3">
          <label class="form-label">Affiliations</label>
          <DynList v-model="authUser.affiliations" ressource="affiliations" />
        </div>
        <div class="mt-2" role="group">
          <button class="btn btn-primary" type="button" @click="updateUser">
            Valider
          </button>
        <div class="btn btn-primary float-end" @click="personalData">
          Télécharger mes données
        </div>
        </div>
      </form>
    </div>
    <modal id="modal-rgpd" v-model="showRGPD" title="RGPD" hide-footer>
      <h6>Conditions d'utilisation</h6>
      <p>
        Pour permettre le bon fonctionnment du site certaines de vos
        informations sont stockées.
      </p>
      <p>
        Nom d'utilisateur, Prénom, Nom, Email sont utilisés afin de vous
        contacter. Seul les managers des entités ont accés à ces informations.
      </p>
      <p>
        Ces informations ainsi que celles liées aux prêts seront stockées 3 ans
        après que vous ayez quitté l'université ou sur demande à l'adresse
        matos@univ-grenoble-alpes.fr
      </p>

      <h6>Accepter vous ces termes ?</h6>
      <div>
        <div class="btn-group" role="group" aria-label="RGPD Accept">
          <button type="button" class="btn btn-primary" @click="accept">
            Oui
          </button>
          <button
            type="button"
            class="btn btn-danger"
            @click="showRGPD = false"
          >
            Non
          </button>
        </div>
      </div>
    </modal>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount, inject } from "vue";
import { useStore } from "vuex";

import DynList from "@/components/ui/DynList.vue";
import Modal from "@/plugins/modal";

const store = useStore();
const showModal = inject("show");

const authUser = computed(() => store.getters.authUser);
const showRGPD = ref(false);
function acceptRGPD() {
  store.dispatch("updateRGPD").then(() => {
    showRGPD.value = false;
    store.dispatch("affiliations/fetchList");
  });
}

async function updateUser() {
  await store.dispatch("updateAuthUser", authUser.value)
          showModal({ content: "Profile mis à jour" });
}
async function personalData() {
  let data = await store.dispatch(USER_DATA);
  let dateObj = new Date();
  let month = dateObj.getMonth() + 1; //months from 1-12
  let day = dateObj.getUTCDate();
  let year = dateObj.getUTCFullYear();
  let labelData = authUser.value.username + "_" + day + month + year + ".json";
  props.totalPages;
  let a = document.createElement("a");
  let file = new Blob([JSON.stringify(data, null, 2)], {
    type: "text/plain",
  });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}
</script>
