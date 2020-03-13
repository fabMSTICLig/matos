export const EditorMixin = {
  data: function() {
    return {
      add: false,
      update: false,
      waiting: false,
      errors: null,
      object: null,
      emptyObject: null,
      actions: {
        GET: "",
        UPDATE: "",
        CREATE: "",
        FETCH: ""
      },
      objectName: ""
    };
  },
  methods: {
    
    handleErrors(e) {
      console.log(e.response);
      this.errors = e.response.data;
      this.waiting = false;
      
      if(e.response.status === 400 ){
          this.$bvModal.msgBoxOk(e.response.data)
      }
    },
    addObject(object) {
      this.object = Object.assign({}, object ? object : this.emptyObject);
      this.add = true;
    },
    selectObject(object) {
      this.$store.dispatch(this.actions.GET, object.id).then(data => {
        this.object = Object.assign({}, data);
        this.update = true;
      });
    },
    saveObject(e) {
      e.preventDefault();
      if (this.update) {
        this.waiting = true;
        console.log(this.actions.UPDATE)
        this.$store
          .dispatch(this.actions.UPDATE, {
            id: this.object.id,
            data: this.object
          })
          .then(data => {
            this.object = Object.assign({}, data);
            console.log(this.objectName + " updated");
            this.$bvModal.msgBoxOk(this.objectName + " updated");
            this.waiting = false;
          })
          .catch(e => {
            this.handleErrors(e);
          });
      } else {
        this.waiting = true;
        this.$store
          .dispatch(this.actions.CREATE, { data: this.object })
          .then(data => {
            this.object = Object.assign({}, data);
            this.add = false;
            this.update = true;
            console.log(this.objectName + " created");
            this.$bvModal.msgBoxOk(this.objectName + " created");
            this.waiting = false;
          })
          .catch(e => {
            this.handleErrors(e);
          });
      }
    }
  },
  beforeMount() {
    this.$store.dispatch(this.actions.FETCH);
  }
};
