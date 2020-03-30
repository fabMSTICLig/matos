<template>
  <div v-if="isAdmin" class="container-fluid mt-4">
          <organization v-if="orga" organization="organization"></organization>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import Organization from './Organization'

import {
  FETCH_ORGAS,
  // eslint-disable-next-line no-unused-vars
  FETCH_AFFILIATIONS
} from '@/store/actions.type'

export default {
  mixins: [EditorMixin],
  name: 'Admin',
  components: {
    Organization
  },
  data () {
    return {
      organization: this.organization || {},

      actions: {
        FETCH: FETCH_ORGAS
      }
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations', 'users', 'isAdmin' ])

  },

  methods: {
    orga () {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      // eslint-disable-next-line eqeqeq
      this.organization = this.orgas.find(orga => orga.id == 18)
      return this.organization
    }
  },

  mounted () { }

}
</script>
