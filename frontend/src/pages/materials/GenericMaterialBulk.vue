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
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h3>{{ currentEntity.name }}: Ajout massif matériel générique</h3>
        </div>
        <div class="card-body">
          <form id="editorForm" class="row g-3">
            <div class="mb-3">
              Format :
              <ul>
                <li>
                  Ordre des champs :
                  <ul>
                    <li>Nom</li>
                    <li>Quantité</li>
                    <li>Référence interne</li>
                    <li>Référence fabriquant</li>
                    <li>Description</li>
                    <li>Localisation</li>
                    <li>Tags</li>
                  </ul>
                </li>
                <li>Encodage : utf8</li>
                <li>Séparateur : tabulation</li>
                <li>Séparateur tags: ',' virgule</li>
              </ul>
            </div>
            <div class="mb-3">
              Télécharger fichier exemple :
              <a href="static/example.csv">example.csv</a>
            </div>
            <div class="custom-file">
              <input
                id="customFile"
                type="file"
                accept=".csv"
                class="custom-file-input"
                @change="changeFile"
              />
            </div>
            <div>
              <span>Fichier : </span
              ><span v-if="file" class="mr-2" v-text="file.name" />
              <button
                v-if="file"
                class="btn btn-danger"
                type="button"
                @click="file = null"
              >
                X
              </button>
            </div>
            <div class="mb-3">
              <label for="textinput">Entrée texte</label>
              <textarea
                id="textarea"
                v-model="textinput"
                class="form-control"
                rows="10"
                :disabled="file"
              />
            </div>
            <div class="col-12">
              <div class="float-end">
                <div class="btn-group" role="group">
                  <button
                    class="btn btn-primary"
                    type="button"
                    @click.prevent="send()"
                  >
                    Ajouter
                  </button>
                  
                  <button
                    class="btn btn-secondary"
                    type="button"
                    @click.prevent="cancel()"
                  >
                    Annuler
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, inject } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { useEntitiesStore } from "@/stores/entities";
import ApiService from "@/helpers/api.service";

const showModal = inject("show");

const entitiesStore = useEntitiesStore();
const { currentEntity } = storeToRefs(entitiesStore);

const file = ref(null);
const textinput = ref(
  "name	quantity	ref_int	ref_fab	desc	loc	tags\narduino uno	10	fabardui	A000073	https://www.arduino.cc/	S03/A1/E3	arduino, elec"
);

function changeFile(f) {
  file.value = f.target.files[0];
}
const route = useRoute();
const router = useRouter();
function send() {
  let data = null;
  let params = {};
  if (file.value) {
    data = new FormData();
    data.append("file", file.value);
    params = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
  } else if (textinput.value) {
    data = new FormData();
    data.append("text", textinput.value);
  }
  if (data) {
    ApiService.post(
      "entities/" + route.params.entityid + "/genericmaterials/bulk_add",
      data,
      params
    )
      .then(() => {
        router.push({
          name: "materialslist",
        });
      })
      .catch((e) => {
        if (e.response) {
          console.log(e.response.data.detail);
          showModal({ content: e.response.data.detail });
        } else console.log(e);
      });
  }
}

function cancel(){
        router.push({
          name: "materialslist",
        });
}
</script>
