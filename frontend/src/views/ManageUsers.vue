<template>
  <div class="home">
    <div class="container">
      <h4>Users management</h4>
      <users v-bind:usersList="usersList"></users>
    </div>
    <hr />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Users from './Users.vue'
import { FETCH_ORGAS, FETCH_USERS } from '@/store/actions.type'
export default {
  name: 'ManageUsers',

  data () {
    return {
      organization: 1
    }
  },
  methods: {
    
  },

  components: {
    Users
  },

  mounted () {
    this.$store.dispatch(FETCH_USERS)
  },

  created () {
    this.$store.dispatch(FETCH_ORGAS)
  },


  computed: {

    ...mapState({
      organizations: state => state.organizations,
      usersList: state => state.users
    }),

    entity () {
      return (
        this.organizations.find(
          organization => organization.id == this.organization
        ) || {}
      )
    },

    items () {
      return [
        { link: 'manage', name: this.entity.name },
        { link: 'manage/users', name: 'Utilisateurs' },
        { link: 'manage/lends', name: 'Prêts en cours' },
        { link: 'manage/history', name: 'Historique de prêts' },
        { link: 'manage/equipments', name: 'Matériels' }
      ]
    }
  }
}
</script>
