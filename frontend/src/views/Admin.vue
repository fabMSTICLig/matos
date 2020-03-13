<template>
  <div>
    <b-card-group rows v-if="update || add">
      <h4>Création d'une entité</h4>
      <b-form @submit="saveEntity()">
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

          <b-row>
            <b-button class="float-right" type="submit" v-show="update" @click.prevent="saveObject" variant="primary">Update</b-button>
            <b-button class="float-right" type="submit" @click.prevent="saveEntity()" v-show="add" variant="primary">Add</b-button>
          </b-row>
        </b-form>
            
      
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
      EmptyObject: { name: null, contact: null, affiliations: [] },
      organization: {
         type: Object,
         default:''
      },

      actions: {
        GET: GET_ORGA,
        UPDATE: UPDATE_ORGA,
        CREATE: CREATE_ORGA,
        FETCH: FETCH_ORGAS
      },
      objectName:'Entity',
      affiliates: []
    };
  },
  computed: {
    ...mapGetters(["orgas", "affiliations","users"]),
        
  },
  methods: {
    saveEntity () {
      console.log("update entity");

        this.$store.dispatch(CREATE_ORGA, { data: this.organization }).then(entity => {
        console.log(entity)
        this.add = false
        this.$router.push({ name: 'update-orga', params: { id: entity.id } })
      }).catch(e =>  {
          if(e.response.status === 400 ){
              console.log(e.response)

              this.$bvModal.msgBoxOk(e.response.data)
          }
      })
    },
    updateManager (manager) {
      this.organization.managed = this.managed
    },
    updateAffiliations (affiliations) {
      this.organization.affiliations = this.affiliates
    },

    emptySelect () {
      this.option = []
      this.$emit('input', "" )
    }
  },

  watch:{
    $route(to, from) {
      console.log(to)
       if (this.$route.params.id) {
      this.update = true
      this.add = false
      let idRoute = this.$route.params.id
      this.organization = this.orgas.find(organization => organization.id == idRoute ) || {}
      this.object = Object.assign({}, this.organization);

      }
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
    this.$store.dispatch(FETCH_AFFILIATIONS)
    this.$store.dispatch(FETCH_USERS)
    this.object = Object.assign({}, this.organization)
    
    

    if (!this.$route.params.id) {
       this.add = true
        console.log(this.object)
    }
     if (this.$route.params.id) {
      this.update = true
      this.add = false
      let idRoute = this.$route.params.id
      this.organization = this.orgas.find(organization => organization.id == idRoute ) || {}
      this.object = Object.assign({}, this.organization);

      }
   

  },
  created() {
    if (this.$route.params.id) {
      this.update = true
      this.add = false
      let idRoute = this.$route.params.id
      this.$store.dispatch(FETCH_ORGAS).then( orgas => {
              this.organization = this.orgas.find(organization => organization.id == idRoute ) || {}

      })

      this.object = Object.assign({}, this.organization);

      }
  }
};
</script>
