<template>
  <div v-if="isAdmin" class="container-fluid mt-4">
    <organization v-if="organizationList" organization="organization"></organization>
    <div v-if="organization.id">
      {{organization.name}}
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import Organization from './Organization'

import {
  FETCH_ORGAS,
  GET_ORGA
  // eslint-disable-next-line no-unused-vars
} from '@/store/actions.type'

export default {
  mixins: [EditorMixin],
  name: 'Admin',
  components: {
    Organization
  },
  actions: {
    GET: GET_ORGA,
    FETCH: FETCH_ORGAS
  },
  data () {
    return {
      organization: this.organization || {},
      organizationList: false,
      actions: {
        FETCH: FETCH_ORGAS
      }
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations', 'users', 'isAdmin' ])
    // eslint-disable-next-line vue/return-in-computed-property

  },

  methods: {
  },
  watch: {
    $route (to, from) {
      console.log(from)
      // eslint-disable-next-line eqeqeq
      if (from.name == 'admin-manageOrga') {
        // eslint-disable-next-line eqeqeq
        // eslint-disable-next-line no-undef
        let id = from.params.id
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == id)
      }
      // eslint-disable-next-line eqeqeq
      if (from.name == 'admin-orga') {
        this.organizationList = true
      }
    }
  },

  beforeMount () {
    console.log(this.$route)
    let self = this
    let routeName = self.$route.name
    this.$store.dispatch(FETCH_ORGAS).then(data => {
      console.log(data)
      // eslint-disable-next-line eqeqeq
      if (routeName == 'admin-manageOrga') {
      // eslint-disable-next-line eqeqeq
      // eslint-disable-next-line no-undef
        let id = this.$route.params.id
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        // eslint-disable-next-line eqeqeq
        console.log(this.orgas)
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == id)
      }
      // eslint-disable-next-line eqeqeq
      if (routeName == 'admin-orga' || routeName == 'update-orga') {
        this.organizationList = true
        console.log('admin orgas')
      }
    })
    // eslint-disable-next-line eqeqeq
  }

}
</script>
