<template>
    <b-container fluid="md-8">
      <b-row class="justify-content-md-center">
        <b-col sm='6'>
          <b-form @submit="onSubmit" @reset="onReset" v-if="show">
          <b-form-group id="input-group-2" label="nom d'utilisateur :" label-for="input-2">
              <b-form-input
              id="input-2"
              v-model="form.username"
              required
              placeholder="Votre nom d'utilisateur"
              ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-2" label="Nom:" label-for="input-2">
              <b-form-input
              id="input-2"
              v-model="form.last_name"
              required
              placeholder="Votre nom"
              ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-2" label="Prénom:" label-for="input-2">
              <b-form-input
              id="input-2"
              v-model="form.first_name"
              required
              placeholder="Votre prénom"
              ></b-form-input>
          </b-form-group>

         <b-form-group
                  label="Affiliations"
                  label-for="select-affiliations"
                  >
                  <b-form-select multiple id="select-affiliations" v-model = "affiliates" :options='affiliationsList' v-on:change="updateAffiliations($event)" v-if="affiliationsList" >
                  </b-form-select>
                </b-form-group>
          <b-form-group
              id="input-group-1"
              label="Email address:"
              label-for="input-1"
              description="email lié à votre compte AGALAN"
          >
              <b-form-input
              id="input-1"
              v-model="form.profile.email"
              type="email"
              required
              placeholder="Enter email"
              ></b-form-input>
          </b-form-group>
          <b-form-group id="input-group-4">
              <b-form-checkbox  v-model="form.profile.acceptance">acceptance RGPD</b-form-checkbox>
          </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
import { EditorMixin } from '@/common/mixins.js'
import { GET_USER, FETCH_USERS, UPDATE_USER } from '@/store/actions.type'

export default {
  name: 'formProfile',
  mixins: [EditorMixin],
  data () {
    return {
      emptyForm: {
        email: '',
        username: '',
        firstname: '',
        lastname: '',
        acceptance: false,
        affiliations: []
      },
      actions: {
        GET: GET_USER,
        UPDATE: UPDATE_USER,
        FETCH: FETCH_USERS
      },
      show: true,
      add: false,
      update: true,
      affiliates: []
    }
  },
  props: {
    object_profile: {
      type: Object,
      default: null
    },
    affiliations: {
      default: null
    }
  },
  watchers: {

  },
  methods: {
    async onSubmit (evt) {
      evt.preventDefault()
      this.assignObject(this.form)
      await this.saveObject(evt)
    },

    updateAffiliations (evt) {
      console.log(evt)
      this.form.profile.affiliations = evt
      console.log(this.form)
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.firstname = ''
      this.form.lastname = null
      this.form.checked = []
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  },

  computed: {
    form () {
      return this.object_profile
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
    }
  },
  beforeMount () {
    let self = this

    this.object_profile.profile.affiliations = this.object_profile.profile.affiliations || {}
    if (this.object_profile.profile.affiliations.length) {
      this.object_profile.profile.affiliations.forEach(function (affiliation) {
        self.affiliates.push(affiliation)
      })
    }
    if (this.object_profile.profile.acceptance) {
      // eslint-disable-next-line no-unused-expressions
      this.object_profile.profile.acceptance.length ? this.form.acceptance = true : false
    }
  }
}
</script>
<style scoped>
.container-md-8 {
  margin-top: 50px;
}
</style>
