
<template>
    <div>
      <organization-list v-if='!isAdmin && !isManager'></organization-list>
      <organization-manage v-if='isAdmin || isManager'></organization-manage>
    </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from 'vuex'
import OrganizationList from '@/views/OrganizationList.vue'
import OrganizationManage from '@/views/OrganizationManage.vue'

export default {
  name: 'Organizations',
  components: { OrganizationList, OrganizationManage },

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
      organizationItem: [],
      organization: this.organization || {},
      objectName: 'Entity',
      affiliates: []
    }
  },
  computed: {
    ...mapState({
      isAdmin: state => state.auth.authUser.is_staff,
      isManager: state => state.auth.authUser.is_manager
    }),
    ...mapGetters(['orgas', 'orga'])
  },
  methods: {

  },

  watch: {
    $route (to, from) {
      // eslint-disable-next-line eqeqeq
      if (to.name == 'organisationsList') {
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
