
<template>
<div>
      <h2>Gestion des entités</h2>
       <b-row>
      <b-col lg="4">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Nom</th>
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody v-if="orgas">
            <tr v-for="entity in orgas" :key="entity.id">
              <td @click="entityManage(entity.id)">{{entity.name}}</td>
              <td class="text-right">
                <a href="#" @click.prevent="editEntity(entity)">Edit</a> -
                <a href="#" @click.prevent="deleteEntity(entity.id)">Delete</a>
              </td>
            </tr>
          </tbody>
        </table>
      </b-col>
      <b-col lg="3">
        <b-card  v-if="update || add">
          <b-form @submit.prevent="saveEntity">
            <b-form-group
              id="label-nom"
              label="Nom"
              label-for="name-input"
            >
            <b-form-input
                type="text"
                id="name-input"
                name="organame"
                v-model="organization.name"
                placeholder="nom"
            />
            </b-form-group>
            <b-form-group
              label="Affiliations"
              label-for="select-affiliations"
              >
              <b-form-select multiple="multiple" id="select-affiliations" v-model = "affiliates" v-on:change="updateAffiliations($event)" v-if="affiliates">
                <option v-for="affiliation in affiliations" :key="affiliation.id" :value="affiliation" :selected="ownAffiliations(affiliation.id)">{{affiliation.name}}</option>
              </b-form-select>
            </b-form-group>
            <b-form-group
              label="contact"
              label-for="contact-input">
              <b-form-input
                id="contact-input"
                type="email"
                placeholder="email contact"
                v-model="organization.contact" />
            </b-form-group>

              <b-row id="actions-btn">
                <b-button type="submit" v-show="update" @click.prevent="saveEntity" variant="primary">Update</b-button>
                <b-button  type="submit" @click.prevent="saveEntity" v-show="add" variant="primary">Add</b-button>
                <b-button id="unselect-btn" variant="outline-primary" @click="deselectAffiliates">Deselect all</b-button>
              </b-row>
           </b-form>
        </b-card>
      </b-col>
        <b-col lg="2">
          <button class="btn btn-info" @click="createLink()">Add new one</button>
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
    async saveEntity (EventForm) {
      this.organization.affiliations = this.affiliates
      this.assignObject(this.organization)
      await this.saveObject(EventForm)
      console.log('entite cree')
      this.fetchData()
    },
    updateManager (manager) {
      this.organization.managed = this.managed
    },
    updateAffiliations (evt) {
      if (this.organization) {
        console.log(evt)
        this.affiliates = evt
      }
    },
    editEntity (entity) {
      this.assignObject(entity)
      // eslint-disable-next-line no-unused-vars
      let id = entity.id
      // eslint-disable-next-line standard/object-curly-even-spacing
      this.$router.push({ path: `/admin/orgas/${id}` })
    },
    deleteEntity (id) {
      this.deleteObject(id)
    },
    deselectAffiliates () {
      this.affiliates = []
      this.organization.affiliations = []
    },
    createLink () {
      this.update = false
      this.add = true
      this.$router.push({ name: 'admin-orga' })
    },
    fetchData () {
      this.$store.dispatch(FETCH_ORGAS)
      this.update = false
      this.add = true
      this.organization = {}
    },
    ownAffiliations (id) {
      // eslint-disable-next-line eqeqeq
      if (this.organization.affiliations) {
      // eslint-disable-next-line eqeqeq
        let ownAffiliation = this.organization.affiliations.find(affiliation => affiliation.id == id)
        console.log(ownAffiliation ? 'true' : '')
        return ownAffiliation ? 'true' : ''
      } else {
        return ''
      }
    },
    entityManage (id) {
      this.$router.push({ path: `/admin/orga/${id}` })
    }
  },

  watch: {
    $route (to, from) {
      if (this.$route.params.id) {
        this.update = true
        this.add = false
        let idRoute = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.affiliates = this.organization.affiliations
      } if (!this.$route.params.id) {
        this.organization = {}
        this.add = true
      }
      this.object = Object.assign({}, this.organization)
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.object = Object.assign({}, this.organization)

    // eslint-disable-next-line eqeqeq
    if (!this.$route.params.id) {
      this.add = true
      console.log(this.object)
    }
    if (this.$route.params.id) {
      this.update = true
      this.add = false
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ORGAS).then(orgas => {
        // eslint-disable-next-line eqeqeq
        this.organization = orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.affiliates = this.organization.affiliations
        console.log('creation')
        console.log(this.object)
      })
    }
  },
  created () {
    this.$store.dispatch(FETCH_ORGAS)

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
