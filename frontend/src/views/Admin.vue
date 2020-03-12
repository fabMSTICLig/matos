<template>
  <div>
    <b-card-group rows v-if="update || add">
      <h4>Création d'une organisation</h4>
      <form action="" @submit="saveEntity(organization)">
        <div class="form-group">
          <label for="organame">nom</label
          ><input
            type="text"
            name="organame"
            v-model="organization.name"
            placeholder="nom"
          />
        </div>
        <div class="form-group">
           <b-form-group label="Affiliations">
          <select multiple="false" v-model="affiliates" v-on:change="updateAffiliations($event.target.value)">
            <option v-for="affiliation in affiliations" :key="affiliation.id" :value="affiliation">{{affiliation.name}}</option>
          </select>
        </b-form-group>
       
        </div>
        <div class="form-group">
          <input type="email" placeholder="email contact" v-model="organization.contact">
        </div>
        
       
        <button class="btn btn-primary" v-if="add" type="submit" @click.prevent="saveEntity(organization)">
          Créer
        </button>
        
        <button class="btn btn-primary" v-if="update" type="submit" @click.prevent="saveEntity(organization)">
          Mise à jour
        </button>
      </form>
    </b-card-group>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from "vuex"
import { EditorMixin } from "@/common/mixins";

import {
  FETCH_ORGAS,
  FETCH_AFFILIATIONS,
  CREATE_ORGA,
  FETCH_USERS
} from "@/store/actions.type";
import { GET_ORGA, UPDATE_ORGA } from '../../../../fac-manager/facmanager/src/store/actions.type';

export default {
  mixins: [EditorMixin],
  name: "Admin",
  components: {},
  data () {
    return {
      organization: {
        type: Object,
        default: ""
      },
      actions:{
        GET: GET_ORGA,
        UPDATE: UPDATE_ORGA,
        CREATE: CREATE_ORGA,
        FETCH: FETCH_ORGAS
      },
      managed: [],
      affiliates: [],
      multiple: "true",
      addAffiliation: false
    };
  },
  computed: {
    ...mapGetters(["orgas", "affiliations","users"]),
    ...mapState({
      affiliations: state => state.affiliations.affiliations,
      organizations: state => state.organizations,
      users: state => state.users
    })
    
  
  },
  methods: {
    saveEntity (entity) {
      console.log("update entity");
      this.$store.dispatch(CREATE_ORGA, { data: entity }).then(entity => {
        console.log(entity)
        this.add = false
        this.$router.push({ name: 'update-orga', params: { id: entity.id } })
      })
    },
    updateManager (manager) {
      this.organization.managed = this.managed
    },
    updateAffiliations (affiliations) {
      this.organization.affiliations = this.affiliates

    },

    emptySelect() {
      this.option = []
      this.$emit('input', "" )
    }
  },
  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.$store.dispatch(FETCH_USERS)
    if (!this.$route.params.id) {
       this.add = true
    }
    if (this.$route.params.id) {
      this.update = true
      this.add = false
      let idRoute = this.$route.params.id
      this.organization = this.organizations.orgas.find(organization => organization.id == idRoute ) || {}

      this.update = true
    }

  }
};
</script>
