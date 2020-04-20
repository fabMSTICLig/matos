
<template>
<div>
    <navbar :items="items"></navbar>
    <entity-list v-if="viewMode" :viewmode="viewMode"></entity-list>
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
              <tbody v-if="entitiesObj">
              <tr v-for="entity in entitiesObj" :key="entity.id">
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
                    v-model="entityObj.name"
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
                    v-model="entityObj.contact" />
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
import EntityList from './EntityList'
import {
  FETCH_ENTITIES,
  FETCH_AFFILIATIONS,
  CREATE_ENTITY,
  GET_ENTITY,
  UPDATE_ENTITY,
  DELETE_ENTITY
} from '@/store/actions.type'

export default {
  mixins: [EditorMixin],
  name: 'EntityManage',
  components: { navbar, EntityList },

  data () {
    return {
      entityObj: this.entityObj || {},
      actions: {
        GET: GET_ENTITY,
        UPDATE: UPDATE_ENTITY,
        CREATE: CREATE_ENTITY,
        FETCH: FETCH_ENTITIES,
        DELETE: DELETE_ENTITY
      },
      viewMode: false,
      objectName: 'Entity',
      update: false,
      add: false,
      affiliates: []
    }
  },
  computed: {
    ...mapGetters([ 'entities', 'affiliations' ]),
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      authUser: state => state.auth.authUser,
      entity: state => state.entities.entity
    }),
    entitiesObj () {
      let self = this
      if (this.isAdmin) {
        return this.entities
      } else {
        console.log(this.entities)
        let entities = this.entities.filter(function (entity) {
          return entity.managed.some(function (user) {
            // eslint-disable-next-line eqeqeq
            return user.id == self.authUser.id
          })
        })
        return entities
      }
    },
    items () {
      return this.isAdmin ? [
        { link: '/entities', name: 'Gestion' },
        { link: '/manage-users', name: 'Utilisateurs' },
        { link: '/entities-list', name: 'Organisation' }
      ]
        : [
          { link: '/entities', name: 'Gestion' },
          { link: '/entities-list', name: 'Organisation' }
        ]
    }
  },
  methods: {
    isManager (managers) {
      // eslint-disable-next-line eqeqeq
      return managers.find(manager => manager.id == this.authUser.id)
    },
    async saveEntity (EventForm) {
      this.entityObj.affiliations = this.affiliates
      this.assignObject(this.entityObj)
      await this.saveObject(EventForm)
      this.fetchData()
    },
    updateManager (manager) {
      this.entityObj.managed = this.managed
    },
    updateAffiliations (evt) {
      if (this.entityObj) {
        console.log(evt)
        this.affiliates = evt
      }
    },
    editEntity (entity) {
      this.assignObject(entity)
      this.$router.push({ path: `/entities/${entity.id}` })
      this.update = true
      this.add = true
    },
    deselectAffiliates () {
      this.affiliates = []
      this.entityObj.affiliations = []
    },
    fetchData () {
      this.$store.dispatch(FETCH_ENTITIES)
    },
    ownAffiliations (id) {
      if (this.entityObj.affiliations) {
      // eslint-disable-next-line eqeqeq
        let ownAffiliation = this.entityObj.affiliations.find(affiliation => affiliation.id == id)
        console.log(ownAffiliation ? 'true' : '')
        return ownAffiliation ? 'true' : ''
      } else {
        return ''
      }
    },
    createLink () {
      this.update = false
      this.add = true
      this.$router.push({ name: 'entities' })
    },
    selectEntity (entity) {
      this.update = true
      this.add = false
      this.$router.push({ path: `/entities/${entity.id}` })
    }
  },

  watch: {
    $route (to, from) {
      this.viewMode = false
      // eslint-disable-next-line eqeqeq
      if (to.name == 'entitiesList') {
        this.viewMode = true
      }
      if (this.$route.params.id) {
        let idRoute = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        this.entityObj = this.entities.find(entity => entity.id == idRoute) || {}
        this.object = Object.assign({}, this.entityObj)
        this.affiliates = this.entityObj.affiliations
        this.update = true
        this.add = false
      } if (!this.$route.params.id) {
        this.update = false
        this.add = true
        this.entityObj = {}
        this.deselectAffiliates()
        this.object = Object.assign({}, this.entityObj)
      }
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.viewMode = false

    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'entitiesList') {
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
      this.$store.dispatch(FETCH_ENTITIES).then(orgas => {
        // eslint-disable-next-line eqeqeq
        this.entityObj = orgas.find(entity => entity.id == idRoute) || {}
        this.object = Object.assign({}, this.entityObj)
        this.affiliates = this.entityObj.affiliations
      })
    }
  },
  created () {
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
