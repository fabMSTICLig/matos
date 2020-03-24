<template>
  <div class="container-fluid mt-4">
    <h2>Gestion des entités</h2>
       <b-row>
      <b-col>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Nom</th>
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody v-if="orgas">
            <tr v-for="entity in orgas" :key="entity.id">
              <td>{{entity.name}}</td>
              <td class="text-right">
                <a href="#" @click.prevent="editEntity(entity)">Edit</a> -
                <a href="#" @click.prevent="deleteEntity(entity.id)">Delete</a>
              </td>
            </tr>
          </tbody>
        </table>
      </b-col>
      <b-col lg="3">
          <organization v-if="orga" organization="organization"></organization>
      </b-col>
    </b-row>
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
    ...mapGetters([ 'orgas', 'affiliations', 'users' ])

  },
  watch: {
    $route (to, from) {
      console.log(to)

      if (this.$route.params.id) {
        this.update = true
        this.add = false
        let idRoute = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == idRoute) || {}
      } if (!this.$route.params.id) {
        this.organization = {}
        // eslint-disable-next-line standard/object-curly-even-spacing
      }
      this.object = Object.assign({}, this.organization)
    }
  },
  methods: {
    orga () {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      // eslint-disable-next-line eqeqeq
      this.organization = this.orgas.find(orga => orga.id == 18)
      return this.organization
    },

    editEntity (entity) {
      this.assignObject(entity)
      // eslint-disable-next-line no-unused-vars
      let id = entity.id
      // eslint-disable-next-line standard/object-curly-even-spacing
      this.$router.push({ path: `/admin/orgas/${id}` })
    }
  },

  mounted () { }

}
</script>
