<template>
  <div class='home'>
    <div class='container'>
      <navbar :items='items' :entity='entity.id'></navbar>
      <organization v-show='isManagement'></organization>

    </div>
    <hr />
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import Organization from './Organization.vue'
import navbar from '@/components/navbar.vue'
import {
  GET_ORGA,
  UPDATE_ORGA,
  CREATE_ORGA,
  FETCH_ORGAS,
  FETCH_EQUIPMENTS
} from '@/store/actions.type'

export default {
  name: 'Manage',
  data () {
    return {
      actions: {
        GET: GET_ORGA,
        UPDATE: UPDATE_ORGA,
        CREATE: CREATE_ORGA,
        FETCH: FETCH_ORGAS
      },
      organization: 1,
      equipmentvue: false,
      loansvue: false,
      usersvue: false,
      historyvue: false
    }
  },
  methods: {
    deleteEquipment (equipment) {
      this.$store.dispatch('deleteEquipment', equipment)
    }
  },

  mounted () {
    this.$store.dispatch('fetchEquipments')
  },
  watch: {
    $route (to, from) {
      this.show = false
      console.log(to)
      // eslint-disable-next-line eqeqeq
      if (this.$route.name == 'manageEntity') {
        console.log('chargement entité')
        this.organization = this.$route.params.id
        this.equipmentvue = false
        this.loansvue = false
        this.historyvue = false
        this.usersvue = false
      }
      // eslint-disable-next-line eqeqeq
      if (this.$route.name == 'manageEquipment-list') {
        console.log('liste equipements')
        this.equipmentvue = !this.equipmentvue
      }
    }
  },

  created () {
    console.log('route')
    console.log(this.$route.name)
  },

  components: {
    Organization,
    navbar
  },
  computed: {
    ...mapGetters(['orgas', 'equipments']),

    ...mapState({
      organizations: state => state.orgas
    }),

    isUsersManagement () {
      // eslint-disable-next-line eqeqeq
      return this.$route.name == 'manageUsers'
    },

    isManagement () {
      let re = /manageEntity/
      let myRoute = this.$route.name.match(re)
      let routeBase = 'manage'
      // eslint-disable-next-line eqeqeq
      if ((myRoute && myRoute.length) || this.$route.name == routeBase) {
        return true
      } else {
        return false
      }
    },

    entity () {
      console.log('entity default')
      console.log(this.organization)
      return (
        this.orgas.find(
          // eslint-disable-next-line eqeqeq
          organization => organization.id == this.$route.params.id
        ) || {}
      )
    },

    items () {
      return [
        { link: '/manage/entity/' + this.entity.id, name: this.entity.name },
        { link: '/manage/users', name: 'Utilisateurs' },
        { link: 'lends', name: 'Prêts en cours' },
        { link: './history', name: 'Historique de prêts' },
        {
          link: '/manage/entity/' + this.$route.params.id + '/equipment-list',
          name: 'Matériels'
        }
      ]
    }
  },
  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
    this.$store.dispatch(FETCH_EQUIPMENTS)
  }
}
</script>
