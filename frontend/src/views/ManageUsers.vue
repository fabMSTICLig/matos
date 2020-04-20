<template>
  <div>
      <navbar :items="items"></navbar>
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
                <b-button variant="primary" @click="addUser"> Add</b-button>
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
import navbar from '@/components/navbar'
import tablecomp from '@/components/table'
import { EditorMixin } from '@/common/mixins'
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
      }
    }
  },
  methods: {
    selectUser (evt) {
      console.log(evt)
    },
    addUser () {
      this.entity.managed.push(this.selectedUser)
      this.$store.dispatch(UPDATE_ENTITY, { id: this.entity.id, data: this.entity }).then((entity) => {
        this.$bvModal.msgBoxOk('Manager added')
          .then(value => {
            this.boxOne = value
          })
          .catch(err => {
            console.log(err)
          })
      })
    },
    async saveEntity (EventForm) {
      this.assignObject(this.entity)
      await this.saveObject(EventForm)
    }
  },

  components: {
    navbar,
    tablecomp
  },

  mounted () {
    this.$store.dispatch(FETCH_USERS)
  },

  created () {
  },

  computed: {
    ...mapGetters([ 'entity', 'entitys', 'users' ]),
    ...mapState({
      entitynizations: state => state.entitynizations,
      managers: state => state.entitynizations.entity.managed
    }),

    items () {
      return [
        { link: '/entitynisations', name: 'Gestion' },
        { link: '/manage-users', name: 'Utilisateurs' },
        { link: '/entitynisations-list', name: 'entitynisation' }
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
