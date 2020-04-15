<template>
    <div v-if="authUser">
        <form-profile :object_profile='profile'></form-profile>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import formProfile from '@/components/formProfile.vue'
export default {
  name: 'profile',
  data () {
    return {
      profile: {
        type: Object,
        default: ''
      }
    }
  },
  components: {
    // eslint-disable-next-line vue/no-unused-components
    formProfile
  },
  computed: {
    ...mapGetters([
      'authUser'
    ])
  },

  beforeMount () {
    if (this.authUser) {
      console.log(this.authUser)
      this.profile = this.authUser.profile
    }
  }

}
</script>
