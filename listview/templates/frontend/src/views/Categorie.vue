<template>
  <div v-if="category" class="display-4 ma-4 d-flex justify-center">
    <select v-model="sorting" v-on:change="sortKey">
      <option v-for="family in categories" :key="family.id" :value="family.id" selected="family.id == 1 ? selected">{{family.title}}</option>
    </select>
   </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'categorie',

  data () {
    return {
      description: '',
      sorting: '1'
    }
  },

  props: {
    family: {
      type: Number,
      default () {
        return ''
      }
    }
  },
  methods: {},
  created () {
    this.$store.dispatch('getCategories')
  },

  computed: {
    category () {
      return this.categories.find(family => family.id == this.family) || {}
 //this.$store.state.category
    },
    ...mapState({
      equipment: state => state.equipment,
      categories: state => state.categories
    }),
    sortKey: {
      get: function () {
        this.$store.dispatch('getCategory', this.sorting.split(' ')[0])
        return this.sorting.split(' ')[0] // return the key part
      }
    },
    sortOrder: {
      get: function () {
        return this.sorting.split(' ')[1] // return the order part
      }
    }
  }
}
</script>
