<template>
  <!--
        Troisième bloc latéral : Plage d'analyse
    -->
  <div class="card m-2">
    <div class="card-header" @click="show = !show">
      <h4>Sélection de la Plage d'analyse/de recherche</h4>
      <p v-if="!show" class="dropdown-toggle">
        <small> Dépliez Moi en cliquant ! </small>
      </p>
      <p v-else class="dropdown-toggle">
        <small> Repliez Moi en cliquant ! </small>
      </p>
    </div>
    <div v-if="show" class="card-body">
      <div class="mb-3" @change="$emit('plageStartDate', startDate)">
        <label class="form-inline-label" for="startDate">
          Date de départ de recherche :
        </label>
        <input
          id="startDate"
          v-model="startDate"
          class="form-inline-control"
          type="date"
          @change="$emit('notChange')"
        />
      </div>
      <div class="mb-3" @change="$emit('plageEndDate', endDate)">
        <label class="form-inline-label" for="endDate">
          Date de fin de recherche :
        </label>
        <input
          id="endDate"
          v-model="endDate"
          class="form-inline-control"
          type="date"
          @change="$emit('notChange')"
        />
      </div>
      <div class="mb-3">
        <select
          id="yearInput"
          v-model="yearInput"
          class="form-inline-control"
          @change="setDateWithYear()"
        >
          <option value="" selected>Choix par Année</option>
          <option
            v-for="year in 3"
            :key="year"
            :value="(dDate.getFullYear() + 1 - year).toString()"
          >
            {{ dDate.getFullYear() + 1 - year }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    startDateDefault: {
      type: String,
      required: true,
    },
    endDateDefault: {
      type: String,
      required: true,
    },
  },
  emits: ["notChange", "plageStartDate", "plageEndDate"],
  data() {
    return {
      show: false,
      startDate: ref(this.startDateDefault),
      endDate: ref(this.endDateDefault),
      dDate: new Date(),
      yearInput: ref(""),
    };
  },
  methods: {
    setDateWithYear() {
      if (this.yearInput != "") {
        this.startDate = this.yearInput + "-01-01";
        this.endDate = this.yearInput + "-12-31";
      }
      this.yearInput = "";
      this.$emit("notChange");
      this.$emit("plageStartDate", this.startDate);
      this.$emit("plageEndDate", this.endDate);
    },
  },
};
</script>
