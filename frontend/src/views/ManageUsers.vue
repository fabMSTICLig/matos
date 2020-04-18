<template>
  <div>
      <navbar :items="items"></navbar>
      <div v-if="orga">
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
import { FETCH_ORGAS, FETCH_USERS, GET_ORGA, UPDATE_ORGA } from '@/store/actions.type'
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
        GET: GET_ORGA,
        UPDATE: UPDATE_ORGA,
        FETCH: FETCH_USERS
      }
    }
  },
  methods: {
    selectUser (evt) {
      console.log(evt)
    },
    addUser () {
      this.orga.managed.push(this.selectedUser)
      this.$store.dispatch(UPDATE_ORGA, { id: this.orga.id, data: this.orga }).then((orga) => {
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
      this.assignObject(this.orga)
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
    ...mapGetters([ 'orga', 'orgas', 'users' ]),
    ...mapState({
      organizations: state => state.organizations,
      managers: state => state.organizations.orga.managed
    }),

    items () {
      return [
        { link: '/organisations', name: 'Gestion' },
        { link: '/manage-users', name: 'Utilisateurs' },
        { link: '/organisations-list', name: 'Organisation' }
      ]
    }
  },
  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
  }
}
</script>
<style scoped>
  .column {
   margin-top: 47px;
 }
</style>
