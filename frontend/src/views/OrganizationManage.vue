
<template>
<div>
    <navbar :items="items"></navbar>
    <organization-list v-if="viewMode" :viewmode="viewMode"></organization-list>
    <b-container v-if="!viewMode">
      <b-row>
        <b-col lg="5">
          <div class='column'>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>&nbsp;</th>
                </tr>
              </thead>
              <tbody v-if="organisations">
              <tr v-for="entity in organisations" :key="entity.id">
                  <td @click="selectEntity(entity)" class="clickRow">{{entity.name}}</td>
                  <td class="text-right">
                    <a href="#" @click.prevent="editEntity(entity)">Edit</a>
                    <span v-if='isAdmin'> - </span>
                    <a href="#" @click.prevent="deleteObject(entity.id)" v-show='isAdmin'>Delete</a>
                  </td>
              </tr>
              </tbody>
            </table>
          </div>
        </b-col>
        <b-col lg="4">
          <div class="column">
            <b-card  v-if="isAdmin || update && !viewMode">
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
                    <b-col>
                      <b-button type="submit" v-show="update" @click.prevent="saveEntity" variant="primary">Update</b-button>
                      <b-button  type="submit" @click.prevent="saveEntity" v-if='isAdmin' v-show="add" variant="primary">Add</b-button>
                    </b-col>
                    <b-col>
                      <b-button id="unselect-btn" variant="outline-primary" @click="deselectAffiliates">Deselect all</b-button>
                    </b-col>
                  </b-row>
              </b-form>
            </b-card>
          </div>
        </b-col>
        <b-col lg="2" v-if="isAdmin">
            <button class="btn btn-info" @click="createLink()" >Add new one</button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import navbar from '@/components/navbar'
import OrganizationList from './OrganizationList'
import Vue from 'vue'
import {
  FETCH_ORGAS,
  FETCH_AFFILIATIONS,
  CREATE_ORGA,
  GET_ORGA,
  UPDATE_ORGA,
  DELETE_ORGA
} from '@/store/actions.type'
var bus = new Vue({})

export default {
  mixins: [EditorMixin],
  name: 'OrganizationManage',
  components: { navbar, OrganizationList },

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
      viewMode: false,
      objectName: 'Entity',
      update: false,
      add: false,
      affiliates: []
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations' ]),
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      authUser: state => state.auth.authUser,
      orga: state => state.organizations.orga
    }),
    organisations () {
      let self = this
      if (this.isAdmin) {
        return this.orgas
      } else {
        let orgas = this.orgas.filter(function (orga) {
          return orga.managed.some(function (user) {
            // eslint-disable-next-line eqeqeq
            return user.id == self.authUser.id
          })
        })
        return orgas
      }
    },
    items () {
      return this.isAdmin ? [
        { link: '/organisations', name: 'Gestion' },
        { link: '/manage-users', name: 'Utilisateurs' },
        { link: '/organisations-list', name: 'Organisation' }
      ]
        : [
          { link: '/organisations', name: 'Gestion' },
          { link: '/organisations-list', name: 'Organisation' }
        ]
    }
  },
  methods: {
    isManager (managers) {
      // eslint-disable-next-line eqeqeq
      return managers.find(manager => manager.id == this.authUser.id)
    },
    async saveEntity (EventForm) {
      this.organization.affiliations = this.affiliates
      this.assignObject(this.organization)
      await this.saveObject(EventForm)
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
      this.$router.push({ path: `/organisations/${entity.id}` })
      this.update = true
      this.add = true
    },
    deselectAffiliates () {
      this.affiliates = []
      this.organization.affiliations = []
    },
    fetchData () {
      this.$store.dispatch(FETCH_ORGAS)
    },
    ownAffiliations (id) {
      if (this.organization.affiliations) {
      // eslint-disable-next-line eqeqeq
        let ownAffiliation = this.organization.affiliations.find(affiliation => affiliation.id == id)
        console.log(ownAffiliation ? 'true' : '')
        return ownAffiliation ? 'true' : ''
      } else {
        return ''
      }
    },
    createLink () {
      this.update = false
      this.add = true
      this.$router.push({ name: 'organisations' })
    },
    selectEntity (entity) {
      this.update = true
      this.add = false
      this.$router.push({ path: `/organisations/${entity.id}` })
    }
  },

  watch: {
    $route (to, from) {
      this.viewMode = false
      // eslint-disable-next-line eqeqeq
      if (to.name == 'organisationsList') {
        this.viewMode = true
      }
      if (this.$route.params.id) {
        let idRoute = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.affiliates = this.organization.affiliations
        this.update = true
        this.add = false
      } if (!this.$route.params.id) {
        this.update = false
        this.add = true
        this.organization = {}
        this.deselectAffiliates()
        this.object = Object.assign({}, this.organization)
      }
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.viewMode = false

    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'organisationsList') {
      this.viewMode = true
    }
    // eslint-disable-next-line eqeqeq
    if (!this.$route.params.id) {
      this.add = true
      this.update = false
    }
    if (this.$route.params.id) {
      this.add = false
      this.update = true
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ORGAS).then(orgas => {
        // eslint-disable-next-line eqeqeq
        this.organization = orgas.find(organization => organization.id == idRoute) || {}
        this.object = Object.assign({}, this.organization)
        this.affiliates = this.organization.affiliations
      })
    }
  },
  created () {
    bus.$on('organization', entity => {
      alert('select')
      this.organization = entity
      this.object = Object.assign({}, this.organization)
    })
  }
}
</script>
<style scoped>

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

</style>
