<template>
  <div>
      <div v-if="entity">
        <b-container fluid="lg">
          <b-row>
            <b-col md="3">
              <div class="column">
                <b-form-select v-model="selectedUser">
                  <b-form-select-option v-for="user in users" :key="user.id" :value="user">{{user.username}}</b-form-select-option>
                </b-form-select>
              </div>
            </b-col>
            <b-col md="2">
                <div class="column">
                  <b-button variant="primary" @click="addUser"> Add</b-button>
                </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col lg="8">
              <div class="column">
                <tablecomp v-if="managers" :items="managers" :actions="true"></tablecomp>
              </div>
            </b-col>
          </b-row>
        </b-container>
      </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import { FETCH_ENTITIES, FETCH_USERS, GET_ENTITY, UPDATE_ENTITY } from '@/store/actions.type'
import tablecomp from '@/components/table'
import { EditorMixin } from '@/common/mixins'
import { bus } from '@/main'
import { DataHelper } from '@/common/helpers'

export default {
  name: 'ManageUsers',
  mixins: [EditorMixin],
  data () {
    return {
      selectedUser: '',
      actions: {
        GET: GET_ENTITY,
        UPDATE: UPDATE_ENTITY,
        FETCH: FETCH_USERS
      },
      messageBox: 'Manager added'
    }
  },
  methods: {
    selectUser (evt) {
      console.log(evt)
    },
    addUser () {
      this.entity.managed.push(this.selectedUser)
      this.saveEntity()
    },
    async saveEntity () {
      this.$store.dispatch(UPDATE_ENTITY, { id: this.entity.id, data: this.entity }).then((entity) => {
        this.$bvModal.msgBoxOk(this.messageBox)
          .then(value => {
            this.boxOne = value
          })
          .catch(err => {
            console.log(err)
          })
      })
    },
    fetchData () {
      this.$store.dispatch(FETCH_ENTITIES)
    }
  },

  components: {
    tablecomp
  },

  mounted () {
    this.$store.dispatch(FETCH_USERS)
  },

  created () {
    let self = this
    bus.$on('removeItem', (item) => {
      self.messageBox = 'Manager removed'
      DataHelper.removeById(self.entity.managed, item)
      self.saveEntity()
    })
  },

  computed: {
    ...mapGetters([ 'entity', 'entities', 'users' ]),
    ...mapState({
      entities: state => state.entities,
      managers: state => state.entities.entity.managed
    }),
    entity () {
      console.log(this.entities)
      // eslint-disable-next-line eqeqeq
      return this.entities.entities.find(entity => entity.id == this.$route.params.id)
    },
    items () {
      return [
        { link: '/entities', name: 'Gestion' },
        { link: '/entities/' + this.$route.params.id + '/users', name: 'Utilisateurs' }
      ]
    }
  },
  beforeMount () {
    this.$store.dispatch(FETCH_ENTITIES)
  }
}
</script>
<style scoped>
  .column {
   margin-top: 47px;
 }
</style>
