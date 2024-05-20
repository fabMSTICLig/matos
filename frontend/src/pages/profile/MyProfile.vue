<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <form
        id="editor-form"
        class="form"
      >
        <div class="mb-3">
          <label
            class="form-label"
            for="username"
          >Username</label><input
            id="username"
            v-model="authUser.username"
            class="form-control"
            type="text"
            readonly
          >
        </div>
        <div class="mb-3">
          <label
            class="form-label"
            for="firstname"
          >Prénom</label><input
            id="firstname"
            v-model="authUser.first_name"
            class="form-control"
            type="text"
            required
            readonly
          >
        </div>
        <div class="mb-3">
          <label
            class="form-label"
            for="lastname"
          >Nom</label><input
            id="lastname"
            v-model="authUser.last_name"
            class="form-control"
            type="text"
            required
            readonly
          >
        </div>
        <div class="mb-3">
          <label
            class="form-label"
            for="email"
          >Email</label><input
            id="email"
            v-model="authUser.email"
            class="form-control"
            type="email"
            required
            readonly
          >
        </div>
        <div
          v-if="authUser.rgpd_accept"
          class="mb-3"
        >
          <label class="form-label">Affiliations</label>
          <DynList
            v-model="authUser.affiliations"
            :ressource="fetchAffs"
          />
        </div>
        <div
          class="mt-2"
          role="group"
        >
          <button
            class="btn btn-primary"
            type="button"
            @click="updateUser"
          >
            Valider
          </button>
          <div
            class="btn btn-primary float-end"
            @click="personalData"
          >
            Télécharger mes données
          </div>
        </div>
      </form>
    </div>
    <modal
      id="modal-rgpd"
      v-model:show="showRGPD"
      title="RGPD"
      hide-footer
    >
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
        <div
          class="btn-group"
          role="group"
          aria-label="RGPD Accept"
        >
          <button
            type="button"
            class="btn btn-primary"
            @click="acceptRGPD"
          >
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
import { ref, inject, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useAffiliationsStore } from "@/stores/affiliations";

import DynList from "@/components/ui/DynList.vue";
import Modal from "@/plugins/modal";

const store = useAuthStore();
const { authUser } = storeToRefs(store);
const showModal = inject("show");

const storeAffiliations = useAffiliationsStore();
const {fetchList: fetchAffs} = storeAffiliations;

const showRGPD = ref(false);
async function acceptRGPD() {
  await store.updateRGPD()
    showRGPD.value = false;
    storeAffiliations.fetchList();
}

onBeforeMount(() => {
  if (!authUser.value.rgpd_accept) {
    showRGPD.value = true;
  }
});

async function updateUser() {
  await store.updateUser(authUser.value);
  showModal({ content: "Profile mis à jour" });
}
async function personalData() {
  let data = await store.getUserData();
  let dateObj = new Date();
  let month = dateObj.getMonth() + 1; //months from 1-12
  let day = dateObj.getUTCDate();
  let year = dateObj.getUTCFullYear();
  let labelData = authUser.value.username + "_" + day + month + year + ".json";
  let a = document.createElement("a");
  let file = new Blob([JSON.stringify(data, null, 2)], {
    type: "text/plain",
  });
  a.href = URL.createObjectURL(file);
  a.download = labelData;
  a.click();
}
</script>
