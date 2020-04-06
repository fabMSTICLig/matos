<template>
  <div v-if="isAdmin" class="container-fluid mt-4">
    <organization v-if="organizationList"></organization>
    <div v-if="organization.id">
        <navbar :items='items' :entity='organization.id'></navbar>
        <template>
          <div v-if="adminUsers && users">
              <b-form class="addUserForm" @submit="onSubmit" @reset="onReset">
                <b-container fluid="lg" class="">
                  <b-row >
                    <b-col>
                      <b-form-group id="input-group-useradd" label="" label-for="input-useradd">
                        <b-dropdown
                          split
                          split-variant="outline-primary"
                          variant="primary"
                          :text="newUser.username || firstUser"
                          class="m-2"
                          block
                        >
                          <b-dropdown-item>
                            <b-form-input
                            id="input-useradd"
                            v-model="newUser.username"
                            required
                            placeholder="Enter name"
                            ></b-form-input>
                          </b-dropdown-item>
                          <b-dropdown-item v-for="user in users" :key="user.id" @click="setUser(user.id)">{{user.username}}</b-dropdown-item>
                        </b-dropdown>
                      </b-form-group>
                    </b-col>
                    <b-col>
                      <b-form-group>
                        <b-button class="centerBt" variant="outline-dark" @click="addUser">Add</b-button>
                      </b-form-group>
                    </b-col>
                    <b-col>
                      <b-button type="submit" @click="onSubmit" class="centerBt" squared variant="dark">Save</b-button>
                    </b-col>
                  </b-row>
                </b-container>
              </b-form>
          </div>
        </template>
        <tablecomp v-if="adminUsers" :items="usersOrganization" :actions="true" v-model="item"></tablecomp>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import { EditorMixin } from '@/common/mixins'
import Organization from './Organization.vue'
import navbar from '@/components/navbar.vue'
import tablecomp from '@/components/table.vue'
import {
  FETCH_ORGAS,
  FETCH_USERS,
  GET_ORGA,
  UPDATE_ORGA
  // eslint-disable-next-line no-unused-vars
} from '@/store/actions.type'
import { bus } from '@/main'

export default {
  mixins: [EditorMixin],
  name: 'Admin',
  components: {
    Organization,
    navbar,
    tablecomp
  },
  data () {
    return {
      organization: this.organization || {},
      newUser: this.newUser || {},
      adminUsers: false,
      addUsers: [],
      item: '',
      organizationList: false,
      actions: {
        FETCH: FETCH_ORGAS,
        UPDATE: UPDATE_ORGA,
        GET: GET_ORGA
      }
    }
  },
  computed: {
    ...mapGetters([ 'orgas', 'affiliations', 'users', 'isAdmin' ]),
    items () {
      return [
        { link: '/admin/orga/' + this.organization.id, name: this.organization.name },
        { link: '/admin/orga/' + this.organization.id + '/users', name: 'Utilisateurs' },
        { link: '/admin/materials', name: 'Matériels' },
        { link: './admin/lends', name: 'Prêts' }
      ]
    },

    firstUser () {
      if (this.users) {
        return 'Utilisateur'
      }
      return ''
    },

    usersOrganization () {
      console.log(this.organization.managed)
      return this.organization.managed
    }

  },

  methods: {
    setUser (id) {
      console.log(id)
      // eslint-disable-next-line eqeqeq
      this.newUser = this.users.find(user => user.id == id)
    },
    async onSubmit (evt) {
      evt.preventDefault()
      this.update = true
      this.assignObject(this.organization)
      await this.saveObject(evt)
      console.log('mise a jour orga ')
      this.fetchData()
    },

    updateUser (item) {
      console.log('obj remove admin')
      console.log(item)
    },

    onReset (evt) {
      evt.preventDefault()
    },

    addUser () {
      this.organization.managed.push(this.newUser)
    },

    removeUser (user) {
      const index = this.organization.managed.indexOf(user)
      if (index > -1) {
        this.organization.managed.splice(index, 1)
      }
    },

    fetchData () {
      this.$store.dispatch(GET_ORGA)
    }
  },
  watch: {
    $route (to, from) {
      // eslint-disable-next-line eqeqeq
      if (to.name == 'admin-manageOrga') {
        let id = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == id)
        this.organizationList = false
      }
      // eslint-disable-next-line eqeqeq
      if (to.name == 'admin-orga') {
        this.organizationList = true
      }
      // eslint-disable-next-line eqeqeq
      if (to.name == 'admin-users') {
        this.$store.dispatch(FETCH_USERS)
        this.adminUsers = true
      }
    }
  },

  beforeMount () {
    console.log(this.$route)
    let self = this
    let routeName = self.$route.name
    this.$store.dispatch(FETCH_ORGAS).then(data => {
    // eslint-disable-next-line eqeqeq
      if (routeName == 'admin-manageOrga') {
        let id = this.$route.params.id
        // eslint-disable-next-line eqeqeq
        this.organization = this.orgas.find(organization => organization.id == id)
      }
      // eslint-disable-next-line eqeqeq
      if (routeName == 'admin-orga' || routeName == 'update-orga') {
        this.organizationList = true
        console.log('admin orgas')
      }

      // eslint-disable-next-line eqeqeq
      if (routeName == 'admin-users') {
        self.$store.dispatch(FETCH_USERS)
        self.adminUsers = true
        let idRoute = self.$route.params.id
        // eslint-disable-next-line eqeqeq
        self.organization = self.orgas.find(orga => orga.id == idRoute)
      }
    })
  },

  created () {
    let self = this
    bus.$on('item', (data) => {
      console.log('remove item')
      self.removeUser(data)
    })
  }

}
</script>
<style scoped>
  .addUserForm {
    width: 800px;
    display: flex;
    flex-direction: row;
  }

  .centerBt {
    margin-top: 9px;
  }

</style>
