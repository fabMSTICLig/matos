<template>
  <div class="home">
    <hr />
    <h4 class="text-center font-weight-bold">Réservation</h4>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',

  components: {
  },

  computed: {
    ...mapGetters(['authUser', 'isAuthenticated', 'isAdmin'])

  }

}
</script>
