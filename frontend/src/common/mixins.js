export const EditorMixin = {
  data: function () {
    return {
      add: false,
      update: false,
      waiting: false,
      errors: null,
      object: null,
      emptyObject: null,
      actions: {
        GET: '',
        UPDATE: '',
        CREATE: '',
        FETCH: '',
        DELETE: ''
      },
      objectName: ''
    }
  },
  methods: {

    handleErrors (e) {
      this.errors = e.response.data
      this.waiting = false

      if (e.response.status === 400) {
        this.$bvModal.msgBoxOk(e.response.data)
      }
    },

    assignObject (object) {
      this.object = Object.assign({}, object)
    },

    selectObject (object) {
      this.$store.dispatch(this.actions.GET, object.id).then(data => {
        this.object = Object.assign({}, data)
        this.update = true
      })
    },
    saveObject (e) {
      e.preventDefault()
      if (this.update) {
        this.waiting = true
        console.log(this.actions.UPDATE)
        console.log(this.object)
        this.$store
          .dispatch(this.actions.UPDATE, {
            id: this.object.id,
            data: this.object
          })
          .then(data => {
            this.object = Object.assign({}, data)
            console.log(this.objectName + ' updated')
            this.$bvModal.msgBoxOk(this.objectName + ' updated')
            this.waiting = false
          })
          .catch(e => {
            this.handleErrors(e)
          })
      } else {
        this.waiting = true
        this.$store
          .dispatch(this.actions.CREATE, { data: this.object })
          .then(data => {
            this.object = Object.assign({}, data)
            this.add = true
            this.update = false
            console.log(this.objectName + ' created')
            this.$bvModal.msgBoxOk(this.objectName + ' created')
            this.waiting = false
          })
          .catch(e => {
            this.handleErrors(e)
          })
      }
    },
    deleteObject (id) {
      this.$store
        .dispatch(this.actions.DELETE, {
          id: id
        })
        .then(data => {
          console.log('object deleted')
          this.$bvModal.msgBoxOk('entity deleted')
          this.waiting = false
        })
        .catch(e => {
          console.log(e)
          this.handleErrors(e)
        })
    }
  },
  beforeMount () {
    this.$store.dispatch(this.actions.FETCH)
  }
}
