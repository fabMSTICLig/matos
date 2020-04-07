<template>
  <div class="home">
    <hr />
    <h4 class="text-center font-weight-bold">Réservation</h4>
    <organization v-if="organizationList"></organization>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Organization from './Organization.vue'

export default {
  name: 'Home',
  data () {
    return {
      organizationList: true

    }
  },
  components: {
    Organization
  },

  computed: {
    ...mapGetters(['authUser', 'isAuthenticated', 'isAdmin'])

  }

}
</script>
