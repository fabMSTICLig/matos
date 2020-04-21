<template>
    <div v-if="authUser">
        <form-profile :object_profile='user' :affiliations="affiliations"></form-profile>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import formProfile from '@/components/formProfile.vue'
import {
  FETCH_AFFILIATIONS
} from '@/store/actions.type'
export default {
  name: 'profile',
  data () {
    return {
      profile: {
        type: Object,
        default: ''
      },
      user: {}
    }
  },
  components: {
    // eslint-disable-next-line vue/no-unused-components
    formProfile
  },
  computed: {
    ...mapGetters([
      'authUser',
      'affiliations'
    ])
  },

  beforeMount () {
    this.$store.dispatch(FETCH_AFFILIATIONS)
    if (this.authUser) {
      console.log(this.authUser)
      this.user.profile = this.authUser.profile || {}
      this.user.externe = this.authUser.externe
      this.user.id = this.authUser.id
      this.user.email = this.authUser.email
      this.user.last_name = this.authUser.last_name
      this.user.first_name = this.authUser.first_name
      this.user.username = this.authUser.username
      this.user.is_staff = this.authUser.is_staff
    }
  }

}
</script>
