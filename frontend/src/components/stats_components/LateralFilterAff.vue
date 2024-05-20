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
  <!--
        Cinquième bloc latéral : Filtrage par type d'affiliation
            Optionnel
    -->
  <div v-if="triValue == 0" class="card m-2">
    <div class="card-header" @click="show = !show">
      <h4>Choix du Filtrage par type d'affiliation</h4>
      <p v-if="!show" class="dropdown-toggle">
        <small> Dépliez Moi en cliquant ! </small>
      </p>
      <p v-else class="dropdown-toggle">
        <small> Repliez Moi en cliquant ! </small>
      </p>
    </div>
    <div v-if="show" class="row">
      <div class="col-sm-6">
        <div class="card-body">
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput0'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="0"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput0'">
              Laboratoire
            </label>
          </div>
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput2'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="2"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput2'">
              Plateforme
            </label>
          </div>
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput4'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="4"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput4'">
              Recherche
            </label>
          </div>
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput6'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="'Naff'"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput6'">
              Sans Affiliation
            </label>
          </div>
        </div>
      </div>
      <div class="col-sm-6">
        <div class="card-body">
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput1'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="1"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput1'">
              Ecole
            </label>
          </div>
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput3'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="3"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput3'">
              Service
            </label>
          </div>
          <div class="form-check" @change="$emit('filterAff', filAffInput)">
            <input
              :id="'filAffInput5'"
              v-model="filAffInput"
              type="checkbox"
              class="form-check-input"
              :value="5"
              @click="$emit('notChange')"
            />
            <label class="form-check-label" :for="'filAffInput5'">
              Composante Universitaire
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    triValue: {
      type: Number,
      required: true,
    },
  },
  emits: ["notChange", "filterAff"],
  data() {
    return {
      show: false,
      filAffInput: ref(["0", "1", "2", "3", "4", "5", "Naff"]),
    };
  },
};
</script>
