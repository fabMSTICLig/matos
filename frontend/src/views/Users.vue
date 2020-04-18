<template>
  <ul class="list-group" v-if="users">
    <li class="list-group-item" v-for="user in users" :key="user.id">{{user.username}}</li>
  </ul>
</template>

<script>

import { mapState } from 'vuex'
import { FETCH_USERS } from '@/store/actions.type'

export default {
  name: 'Users',
  methods: {

  },
  computed: {
    ...mapState({
      users: state => state.users.users
    })
  },
  beforeMount () {
    this.$store.dispatch(FETCH_USERS)
  }
}
</script>
