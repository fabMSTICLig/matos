<template>
  <ul class="list-group" v-if="users">
    <li class="list-group-item" v-for="user in users" :key="user.id">{{user.username}}</li>
   </ul>
</template>

<script>
  
  import { mapState } from "vuex"

  export default {
    name: "Users",
    methods: {
      
    },
    computed: {
      ...mapState({
        users: state => state.users
      })
    },
    beforeMount() {
          this.$store.dispatch("getUsers");

    }
  };
</script>
