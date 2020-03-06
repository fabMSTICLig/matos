<template>
  <div v-if="categories" class="ma-4 d-flex justify-center">
    <span>Selected: {{ selectedItems }}</span>
    <select multiple v-model="selectedItems" v-on:change="updateValue($event.target.value)"
     v-bind:value="value">
      <option v-for="family in familiesList" :value="family.value" :key="family.id" >{{family.text}}</option>
    </select>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from "vuex";
import Vue from "vue"

export default {
  name: "categorie",

  data() {
    return {
      description: "",
      sorting: "1",
      selectedItems: []
    };
  },
  props: [
    'value'
  ],
 
  methods: {
    selectedFamily(id) {
      return this.families.find(family => family.id == id) || {};
    },

    updateValue(value) {

      
      console.log(this.selectedItems)
      this.$emit('input', this.selectedItems);
    }
  },
  created() {
    this.$store.dispatch("getCategories");
  },

  computed: {
    ...mapState({
      equipment: state => state.equipment,
      categories: state => state.categories
    }),

    familiesList() {
      let families = []
      for (let i = 0; i <= this.categories.length - 1; i++) {
        let family = {
          text: this.categories[i].title,
          value: this.categories[i]
        };
        families.push(family);
      }

      return families;
    },

    
  }
};
</script>
