
<template>
    <div v-if="entityObj">
      <entity-manage v-if='isAdmin || isManaged()' :entity="entityObj"></entity-manage>
      <b-container>
        <b-row>
          <b-col lg="5">
            <div class="column">
              <entity v-if="!isAdmin && !isManaged()" :entity="entityObj"></entity>
            </div>
          </b-col>
       </b-row>
    </b-container>
    </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import EntityManage from '@/views/EntityManage.vue'
import Entity from '@/components/entity.vue'
import { FETCH_ENTITIES } from '@/store/actions.type'

export default {
  name: 'Entities',
  components: { EntityManage, Entity },
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
      entityItem: [],
      objectName: 'Entity',
      affiliates: [],
      detail: true
    }
  },
  computed: {
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      isManager: state => state.auth.authUser.is_manager
    }),
    ...mapGetters(['entities', 'entity', 'authUser']),

    entityObj () {
      console.log(this.entities)
      // eslint-disable-next-line eqeqeq
      console.log(this.entities.find(entity => entity.id == this.$route.params.id))
      // eslint-disable-next-line eqeqeq
      return this.entities.find(entity => entity.id == this.$route.params.id)
    }
  },
  methods: {
    isManaged () {
      let self = this
      console.log(this.entityObj)

      // eslint-disable-next-line eqeqeq
      let managed = this.entityObj.managed.some(function (user) {
        // eslint-disable-next-line eqeqeq
        console.log(user.id == self.authUser.id)
        // eslint-disable-next-line eqeqeq
        return user.id == self.authUser.id
      })
      return managed
    }
  },

  watch: {
    $route (to, from) {
      // eslint-disable-next-line eqeqeq
      if (to.name == 'entitiesList') {
        this.viewMode = true
      }
      if (this.$route.params.id) {

      } if (!this.$route.params.id) {
      }
    }
  },
  beforeMount () {
    this.$store.dispatch(FETCH_ENTITIES)
    // eslint-disable-next-line eqeqeq
    if (this.$route.name == 'entity') {
      this.detail = true
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
</style>
