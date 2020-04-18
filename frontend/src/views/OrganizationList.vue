
<template>
  <b-container>
      <b-row>
        <b-col lg="5">
          <div class="column">
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
          </div>
        </b-col>
        <b-col md="3" v-if="object.id">
          <div class="column">
            <organization :organization="object"  v-on:input="selectOrganization"></organization>
          </div>
        </b-col>
       </b-row>
  </b-container>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import organization from '@/components/organization.vue'

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
  name: 'OrganizationList',
  components: {
    organization
  },

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
  props: {
    viewmode: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations' ])

  },
  methods: {

    entityView (entity) {
      // this.selectObject(entity)
      this.organizationItem = []
      if (!this.viewmode) {
        this.$router.push({ path: `/organisations/${entity.id}` })
      }
      if (this.viewmode) {
        console.log(entity)
        this.object = entity
        console.log(this.object)
      }
    },
    fetchData () {
      this.$store.dispatch(FETCH_ORGAS)
      this.organization = {}
    },
    selectOrganization (entity) {
      alert('select')
      this.organization = entity
      this.object = Object.assign({}, this.organization)
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
    let self = this
    if (this.$route.params.id) {
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ORGAS).then(orgas => {
        // eslint-disable-next-line eqeqeq
        self.organization = orgas.find(organization => organization.id == idRoute) || {}
        self.object = Object.assign({}, this.organization)
        self.affiliates = this.organization.affiliations // this.organizationItem.push(this.object)
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
 .column {
   margin-top: 47px;
 }

 th {
   border:none;
  }

  .row > :nth-child(2) {
    margin-top: 50px;
  }

</style>
