
<template>
<div>
      <h2>Liste des entités</h2>
       <b-row>
        <b-col lg="5">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Nom</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody v-if="orgas">
              <tr v-for="entity in orgas" :key="entity.id">
                <td @click="entityView(entity)" class="clickRow">{{entity.name}}</td>
                <td class="text-right">
                  <b-button @click="entityView(entity)">View</b-button>
                </td>
              </tr>
            </tbody>
          </table>
        </b-col>
        <b-col md="3" v-if="organizationItem">
          <b-table
            :borderless="borderless"
            :items="organizationItem"
            :fields="fields"
            :head-variant="headVariant"
            :table-variant="tableVariant"
          ></b-table>
        </b-col>
       </b-row>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'

import {
  FETCH_ORGAS,
  FETCH_AFFILIATIONS,
  CREATE_ORGA,
  GET_ORGA,
  UPDATE_ORGA,
  DELETE_ORGA
} from '@/store/actions.type'

export default {
  mixins: [EditorMixin],
  name: 'Organization',
  components: {},

  data () {
    return {
      fields: [
        { key: 'name', label: 'Nom', sortable: false, class: 'text-center' },
        { key: 'contact', label: 'Contact', sortable: true, class: 'text-center' },
        { key: 'description', label: 'Description', sortable: false, class: 'text-center' }
      ],
      borderless: true,
      headVariant: 'dark',
      tableVariant: 'light',
      organizationItem: [],
      organization: this.organization || {},
      actions: {
        GET: GET_ORGA,
        UPDATE: UPDATE_ORGA,
        CREATE: CREATE_ORGA,
        FETCH: FETCH_ORGAS,
        DELETE: DELETE_ORGA
      },
      objectName: 'Entity',
      affiliates: []
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations' ])

  },
  methods: {

    entityView (entity) {
      this.selectObject(entity)
      this.organizationItem = []
      this.$router.push({ path: `/orga/${entity.id}` })
    },
    fetchData () {
      this.$store.dispatch(FETCH_ORGAS)
      this.organization = {}
    }

  },

  watch: {
    $route (to, from) {
      if (this.$route.params.id) {
        let idRoute = this.$route.params.id
        console.log(this.organization)
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.organizationItem.push(this.object)
      } if (!this.$route.params.id) {
        this.organization = {}
      }
      this.object = Object.assign({}, this.organization)
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.object = Object.assign({}, this.organization)

    if (this.$route.params.id) {
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ORGAS).then(orgas => {
        // eslint-disable-next-line eqeqeq
        this.organization = orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.affiliates = this.organization.affiliations
        this.organizationItem.push(this.object)
        console.log(this.object)
      })
    }
  },
  created () {
    if (this.$route.params.id) {
      this.update = true
      this.add = false
      this.affiliates = this.organization.affiliations
    }
  }
}
</script>
<style scoped>
 #unselect-btn {
   margin-left: 20px;
 }
 #actions-btn {
   display: flex;
   justify-content: space-between;
 }
 #actions-btn > button {
   width: auto;
   height: 35px;
 }
</style>
