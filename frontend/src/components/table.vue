<template>
  <div>
    <b-table striped hover
      :items="items"
      :fields="fields"
      :current-page="currentPage"
      :per-page="perPage"
      :filter="filter"
      :filterIncludedFields="filterOn"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      :sort-direction="sortDirection"
      @filtered="onFiltered"
      >
      <template v-slot:cell(username)="scope" v-if="busy">
        <input type="text" class="form-control-sm"
                           style="width:5em"
                           :value="scope.item.username"
                           v-on:input="handleUsername($event, scope.item, scope.index)"
                           @blur="stopEditing"/>
      </template>

      <template v-slot:cell(actions)="row" v-if="actions">
        <b-container fluid>
          <b-row>
            <b-col sm="1">
              <b-button :id="'remove-user-' + row.index" @click="removeObj(row.item)" size="sm" variant="danger">
              -
              </b-button>
            </b-col>
          </b-row>
        </b-container>
      </template>
    </b-table>
    <!-- Info modal -->
  </div>
</template>

<script>
import { bus } from '@/main'

export default {
  name: 'tablecomp',
  data () {
    return {
      visible: false,
      busy: false,
      fields: [
        { key: 'id', label: 'Id', sortable: false, sortDirection: 'desc' },
        { key: 'username', label: 'Username', sortable: false, class: 'text-center' },
        { key: 'email', label: 'Email', sortable: true, class: 'text-center' },
        { key: 'first_name', label: 'Firstname', sortable: false, class: 'text-center' },
        { key: 'last_name', label: 'Lastname', sortable: true, class: 'text-center' },
        { key: 'is_staff', label: 'Is Staff', sortable: false, class: 'text-center' },
        { key: 'actions', label: 'Actions' }
      ],
      totalRows: 1,
      currentPage: 1,
      perPage: 5,
      pageOptions: [5, 10, 15],
      sortBy: '',
      sortDesc: false,
      sortDirection: 'asc',
      filter: null,
      filterOn: [],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      }
    }
  },
  props: {
    title: {
      type: String,
      default: 'toggle'
    },
    items: {
      type: Array
    },
    actions: {
      type: Boolean,
      default: false
    }
  },

  computed: {},

  mounted () {
    this.totalRows = this.items.length
  },

  methods: {

    stopEditing: function (evt) {
      console.log('stop editing')
      this.busy = !this.busy
    },

    info (item, index, button) {
      this.infoModal.title = `Row index: ${index}`
      this.infoModal.content = JSON.stringify(item, null, 2)
      this.$root.$emit('bv::toggle::collapse', 'actions-list-' + index)
    },
    handleUsername (evt, item, index) {
      let value = evt.target.value
      console.log(item)

      item.username = value
      bus.$emit('item', item)
    },

    removeObj (item) {
      console.log('removeObje')
      console.log(item)
      bus.$emit('removeItem', item)
    },

    editMode () {
      this.busy = !this.busy
    },

    resetInfoModal () {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
    onFiltered (filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    }
  }
}
</script>
