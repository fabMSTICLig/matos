
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
              <tbody v-if="entities">
                <tr v-for="entity in entities" :key="entity.id">
                  <td @click="entityView(entity)" class="clickRow">{{entity.name}}</td>
                  <td class="text-right">
                    <a href="#" v-if="isManager(entity) || isAdmin" @click.prevent="manageEntity(entity)">Edit</a>
                    <span v-if='isAdmin'> - </span>
                    <a href="#" @click.prevent="deleteObject(entity.id)" v-show='isAdmin'>Delete</a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </b-col>
        <b-col md="3" v-if="object.id">
          <div class="column">
            <entity :entity="object"  v-on:input="selectEntity"></entity>
          </div>
        </b-col>
        <b-col lg="2" v-if="isAdmin">
            <button class="btn btn-info" @click="createLink()" >Add new one</button>
        </b-col>
       </b-row>
  </b-container>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import entity from '@/components/entity.vue'

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
  name: 'EntityList',
  components: {
    entity
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
      entityObj: this.entityObj || {},
      actions: {
        GET: GET_ENTITY,
        UPDATE: UPDATE_ENTITY,
        CREATE: CREATE_ENTITY,
        FETCH: FETCH_ENTITIES,
        DELETE: DELETE_ENTITY
      },
      objectName: 'Entity',
      affiliates: [],
      newEntity: false
    }
  },
  props: {
    viewmode: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters([ 'entities', 'affiliations' ]),
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      authUser: state => state.auth.authUser
    })
  },
  methods: {
    isManager (entity) {
      let self = this
      console.log(entity.managed)
      return entity.managed.find(function (user) {
        // eslint-disable-next-line eqeqeq
        return user.id == self.authUser.id
      })
    },
    entityView (entity) {
      if (!this.viewmode) {
        this.$router.push({ path: `/entities/${entity.id}` })
      }
      if (this.viewmode) {
        console.log(entity)
        this.object = entity
        console.log(this.object)
      }
    },
    fetchData () {
      this.$store.dispatch(FETCH_ENTITIES)
      this.entityObj = {}
    },
    selectEntity (entity) {
      this.entityObj = entity
      this.object = Object.assign({}, this.entityObj)
    },
    manageEntity (entity) {
      this.$router.push({ path: `/entities/${entity.id}` })
    },
    createLink () {
      this.update = false
      this.add = true
      this.$router.push({ path: `/entities/create` })
    }

  },

  watch: {
    $route (to, from) {
      if (this.$route.params.id) {
        let idRoute = this.$route.params.id
        console.log(this.entityObj)
        // eslint-disable-next-line eqeqeq
        this.entityObj = this.entities.find(entity => entity.id == idRoute) || {}
        this.object = Object.assign({}, this.entityObj)
        this.entityObjItem.push(this.object)
      } if (!this.$route.params.id) {
        this.entityObj = {}
      }
      this.object = Object.assign({}, this.entityObj)
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_ENTITIES)
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.object = Object.assign({}, this.entityObj)
    let self = this
    if (this.$route.params.id) {
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ENTITIES).then(entities => {
        // eslint-disable-next-line eqeqeq
        self.entity = entities.find(entity => entity.id == idRoute) || {}
        self.object = Object.assign({}, this.entityObj)
        self.affiliates = this.entityObj.affiliations // this.entityObjItem.push(this.object)
        console.log(this.object)
      })
    }
  },
  created () {
    if (this.$route.params.id) {
      this.update = true
      this.add = false
      this.affiliates = this.entityObj.affiliations
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
