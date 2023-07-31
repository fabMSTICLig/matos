<template>
  <!--
        Sixième bloc latéral : Filtrage sur fréquence
            Optionnel
    -->
  <div v-if="(statValue == 'freq_emp') & (triValue != 1)" class="card m-2">
    <div class="card-header" @click="show = !show">
      <h4>Choix du Filtrage sur fréquence</h4>
      <p v-if="!show" class="dropdown-toggle">
        <small> Dépliez Moi en cliquant ! </small>
      </p>
      <p v-else class="dropdown-toggle">
        <small> Repliez Moi en cliquant ! </small>
      </p>
    </div>
    <div v-if="show" class="card-body">
      <div class="form-check mb-1" @change="$emit('filterFreq', filFreqInput)">
        <input
          :id="'filFreqInput0'"
          v-model="filFreqInput"
          type="radio"
          class="form-check-input"
          :value="0"
          @click="$emit('notChange')"
        />
        <label class="form-check-label" :for="'filFreqInput0'">
          Aucun Filtrage
        </label>
      </div>
      <div class="form-check mb-1" @change="$emit('filterFreq', filFreqInput)">
        <input
          :id="'filFreqInput1'"
          v-model="filFreqInput"
          type="radio"
          class="form-check-input"
          :value="1"
          @click="$emit('notChange')"
        />
        <label class="form-check-label" :for="'filFreqInput1'">
          Empruntés uniquement
        </label>
      </div>
      <div class="form-check mb-1" @change="$emit('filterFreq', filFreqInput)">
        <input
          :id="'filFreqInput2'"
          v-model="filFreqInput"
          type="radio"
          class="form-check-input"
          :value="2"
          @click="$emit('notChange')"
        />
        <label class="form-check-label" :for="'filFreqInput2'">
          Jamais empruntés uniquement
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    statValue: {
      type: String,
      required: true,
    },
    triValue: {
      type: Number,
      required: true,
    },
  },
  emits: ["notChange", "filterFreq"],
  data() {
    return {
      show: false,
      filFreqInput: ref("0"),
    };
  },
};
</script>
