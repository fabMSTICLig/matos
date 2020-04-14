<template>
  <div v-if="categories" class="ma-4 d-flex justify-center">
    {{option}}
    <select multiple="multiple" v-model="option" v-on:change="updateValue($event.target.value)"
     v-bind:value="value" v-if="value">
      <option v-for="family in familiesList" :value="family.value" :key="family.id" :selected="isFamily(family)">{{family.text}}</option>
    </select>
    <button @click="emptySelect()" >reset</button>

  </div>
</template>

<script>

// selected --> init value //

// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'categorie',
  props: [
    'value'
  ],
  data () {
    return {
      option: '',
      description: '',
      sorting: '1'
    }
  },

  methods: {

    isFamily (val) {
      console.log(val.value.id)
      console.log(this.value)

      // eslint-disable-next-line eqeqeq
      let familyEquipment = this.value.find(family => family.id == val.value.id)
      return familyEquipment ? 'selected' : ''
    },

    emptySelect () {
      this.option = []
      this.$emit('input', '')
    },
    updateValue (value) {
      console.log(value)
      // this.option = value
      // this.option.push( value)
      this.$emit('input', this.option)
    }

  },
  created () {
    this.$store.dispatch('getCategories')
    console.log(this.value)
  },

  computed: {
    ...mapState({
      equipment: state => state.equipment,
      categories: state => state.categories
    }),
    getCurrentFamilies () {
      return this.value
    },

    familiesList () {
      let families = []
      for (let i = 0; i <= this.categories.length - 1; i++) {
        let family = {
          text: this.categories[i].title,
          value: this.categories[i]
        }
        families.push(family)
      }

      return families
    }

  }
}
</script>
