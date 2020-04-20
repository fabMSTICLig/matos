<template>
    <div v-if="authUser">
        <form-profile :object_profile='profile' :affiliations="affiliations"></form-profile>
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
      }
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
      this.profile = this.authUser.profile
      this.profile.username = this.authUser.username
      this.profile.lastname = this.authUser.last_name
      this.profile.firstname = this.authUser.first_name
    }
  }

}
</script>
