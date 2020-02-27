<template>
  <div v-if="entity">
      <h4 class="text-center font-weight-bold">{{entity.name}}</h4>
    <label>Nom </label> <input type="text" v-model="entity.name" placeholder="entity.name">
    <label>Contact </label><input type="text" v-model="entity.contact" placeholder="entity.contact">
    <label>Type d'entité</label>
    <select v-model="sorting" v-on:change="sortKey">
        <option v-for="type in orgatypes" :key="type.id" :value="type.id" selected="type.id == entity.orga_type ? selected">
            {{type.name}}
        </option>
    </select>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'Organization',

  data () {
    return {
      sorting: '1'
    }
  },

  props: {
    organization: {
      type: Number,
      default () {
        return ''
      }
    }
  },
  methods: {},
  created () {
    this.$store.dispatch('getOrganizations')
    this.$store.dispatch('getOrganizationTypes')

  },

  computed: {
    entity () {
      return this.organizations.find(organization => organization.id == this.organization) || {}
    },

    orgatype () {
      return this.orgatypes.find(organizationtype => organizationtype.id == this.entity.orgatype.id) || {}
    },

    ...mapState({
      equipment: state => state.equipment,
      organizations: state => state.organizations,
      orgatypes: state => state.organizationTypes

    }),
    sortKey: {
      get: function () {
        this.$store.dispatch('getOrganizationTypes', this.sorting.split(' ')[0])
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
