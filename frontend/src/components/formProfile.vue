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
              v-model="form.lastname"
              required
              placeholder="Votre nom"
              ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-2" label="Prénom:" label-for="input-2">
              <b-form-input
              id="input-2"
              v-model="form.firstname"
              required
              placeholder="Votre prénom"
              ></b-form-input>
          </b-form-group>
          <b-form-group
              id="input-group-1"
              label="Email address:"
              label-for="input-1"
              description="email lié à votre compte AGALAN"
          >
              <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              required
              placeholder="Enter email"
              ></b-form-input>
          </b-form-group>
          <b-form-group id="input-group-4">
              <b-form-checkbox  v-model="form.acceptance">acceptance RGPD</b-form-checkbox>
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
        acceptance: false
      },
      actions: {
        GET: GET_USER,
        UPDATE: UPDATE_USER,
        FETCH: FETCH_USERS
      },
      show: true,
      add: false,
      update: true
    }
  },
  props: {
    object_profile: {
      type: Object,
      default: null
    }
  },
  watchers: {
    object_profile (value) {
      console.log('update value')
      console.log(value)
    }
  },
  methods: {
    async onSubmit (evt) {
      evt.preventDefault()
      this.assignObject(this.form)
      await this.saveObject(evt)
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.name = ''
      this.form.food = null
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
      return this.object_profile || this.emptyForm
    }
  }
}
</script>
<style scoped>
.container-md-8 {
  margin-top: 50px;
}
</style>
