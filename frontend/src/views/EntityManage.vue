
<template>
<div>
    <navbar v-if="isAdmin && !createEntity && items" :items="items"></navbar>
    <b-container v-if="manageEntity || add">
      <b-row>
        <b-col lg="4">
          <div class="column">
            <b-card  v-if="isAdmin || isManaged">
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
                  <b-form-select multiple id="select-affiliations" v-model = "affiliates" :options='affiliationsList' v-on:change="updateAffiliations($event)" v-if="affiliationsList" >
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
        <b-col>
            <div class="column">
              <entity v-if="entityObj.id" :entity="entityObj"></entity>
            </div>
        </b-col>
      </b-row>
    </b-container>
    <router-view></router-view>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import navbar from '@/components/navbar'
import entity from '@/components/entity'
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
  components: { navbar, entity },

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
      manageEntity: false,
      objectName: 'Entity',
      update: false,
      add: false,
      affiliates: [],
      createEntity: false
    }
  },
  props: {
    entity: {
      type: Object,
      default: null
    }
  },
  computed: {
    ...mapGetters([ 'entities', 'affiliations' ]),
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      authUser: state => state.auth.authUser
    }),
    isManaged () {
      let self = this
      return this.entity.managed.some(function (user) {
        // eslint-disable-next-line eqeqeq
        return user.id == self.authUser.id
      })
    },
    affiliationsList () {
      let values = this.affiliations.map(
        affiliation => {
          let option = {}
          option['value'] = affiliation
          option['text'] = affiliation.name
          return option
        })
      return values
    },
    items () {
      return [
        { link: '/entities/' + this.$route.params.id, name: 'Gestion' },
        { link: '/entities/' + this.$route.params.id + '/users', name: 'Utilisateurs' }
      ]
    }
  },
  methods: {
    async saveEntity (EventForm) {
      this.entityObj.affiliations = this.affiliates
      this.assignObject(this.entityObj)
      await this.saveObject(EventForm)
      await this.fetchData()
    },
    updateAffiliations (evt) {
      if (this.entityObj) {
        console.log(evt)
        this.affiliates = evt
      }
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
        return ownAffiliation ? 'selected' : ''
      } else {
        return ''
      }
    }
  },

  watch: {
    $route (to, from) {
      // eslint-disable-next-line eqeqeq
      if (to.name == 'createEntity') {
        this.manageEntity = false
        this.createEntity = true
      }
      // eslint-disable-next-line eqeqeq
      if (to.name == 'manageUsers') {
        this.createEntity = false
        this.manageEntity = false
      }

      // eslint-disable-next-line eqeqeq
      if (to.name == 'entity') {
        this.manageEntity = true
      }

      if (this.$route.params.id) {
        this.object = Object.assign({}, this.entity)
        this.affiliates = this.entity.affiliations
        this.update = true
        this.add = false
      } if (!this.$route.params.id) {
        this.update = false
        this.add = true
        this.entityObj = {}
        this.object = Object.assign({}, this.entityObj)
      }
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_AFFILIATIONS)

    if (this.$route.name !== 'entity' && this.$route.name !== 'createEntity') {
      this.manageEntity = false
    }
    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'entity') {
      this.manageEntity = true
      this.affiliates = this.entity.affiliations
    }
    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'manageUsers') {
      this.manageEntity = false
      this.add = false
    }

    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'createEntity') {
      this.add = true
      this.update = false
      this.createEntity = true
    }

    if (this.$route.params.id) {
      this.add = false
      this.update = true
      this.entityObj = this.entity
    }
    if (!this.$route.params.id) {
      this.add = true
      this.update = false
      this.entityObj = {}
      this.object = Object.assign({}, this.entityObj)
    }
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
