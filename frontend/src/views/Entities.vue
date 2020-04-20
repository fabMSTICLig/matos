
<template>
    <div>
      <entity-list v-if='!isAdmin && !isManager'></entity-list>
      <entity-manage v-if='isAdmin || isManager'></entity-manage>
    </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import EntityList from '@/views/EntityList.vue'
import EntityManage from '@/views/EntityManage.vue'

export default {
  name: 'Entities',
  components: { EntityList, EntityManage },

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
      entityObj: this.entityObj || {},
      objectName: 'Entity',
      affiliates: []
    }
  },
  computed: {
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      isManager: state => state.auth.authUser.is_manager
    }),
    ...mapGetters(['entities', 'entity'])
  },
  methods: {

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
    // eslint-disable-next-line no-undef

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
</style>
