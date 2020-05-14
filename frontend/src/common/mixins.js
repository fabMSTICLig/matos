import Pagination from "@/components/Pagination";
import { PUSH_BREADCUMB, POP_BREADCUMB } from "@/store/actions.type";

export const ListMixin = {
  components: {
    Pagination
  },

  data: function() {
    return {
      ressource: "",
      search_input: "",
      search_fields: [],
      current_page: 1,
      selected_object: null
    };
  },
  computed: {
    objects_list() {
      return this.$store.getters[this.ressource + "/list"];
    },
    objects_filtered() {
      if (typeof this.search_fields === "function") {
        return this.search_fields(this.objects_list, this.search_input);
      } else {
        return this.objects_list.filter(item => {
          return this.search_fields.some(field => {
            return (
              item[field]
                .toLowerCase()
                .indexOf(this.search_input.toLowerCase()) > -1
            );
          });
        });
      }
    },
    objects_paginated() {
      return this.objects_filtered.slice(
        (this.current_page - 1) * process.env.VUE_APP_MAXLIST,
        this.current_page * process.env.VUE_APP_MAXLIST
      );
    },
    pages_count() {
      return Math.ceil(
        this.objects_filtered.length / process.env.VUE_APP_MAXLIST
      );
    }
  },
  methods: {
    onPageChange(page) {
      this.current_page = page;
    },
    initList() {
      this.$store.dispatch(this.ressource + "/fetchList").then(() => {
        if (this.objects_list.length > 0) {
          this.selected_object = this.objects_list[0];
        }
      });
    },
    initComponent() {
      return Promise.resolve();
    }
  },
  beforeMount() {
    this.initComponent().then(() => {
      this.initList();
    });
  }
};

export const EditMixin = {
  data() {
    return {
      ressource: "",
      breadcumb: {},
      object: null,
      new_label: "",
      object_name: ""
    };
  },
  computed: {
    is_new() {
      return this.$route.path.indexOf("new") > -1;
    },
    cardName() {
      return this.is_new ? this.new_label : this.breadcumb.label;
    }
  },
  methods: {
    get_empty() {
      return {};
    },
    make_label() {
      return "";
    },
    initComponent() {
      return Promise.resolve();
    },
    initObject(route) {
      if (route.params.id == "new") {
        this.object = this.get_empty();
        this.$store.dispatch(PUSH_BREADCUMB, {
          label: "Création",
          url: route.path
        });
      } else if (parseInt(route.params.id, -1) != -1) {
        this.$store
          .dispatch(this.ressource + "/fetchSingle", route.params.id)
          .then(data => {
            this.object = Object.assign({}, data);
            this.breadcumb = {
              label: this.make_label(),
              url: route.path
            };
            this.$store.dispatch(PUSH_BREADCUMB, this.breadcumb);
          });
      }
    },
    update() {
      if (document.querySelector("#editor-form").checkValidity()) {
        this.$store
          .dispatch(this.ressource + "/update", {
            id: this.object.id,
            data: this.object
          })
          .then(data => {
            this.object = Object.assign({}, data);
            console.log(this.object_name + " updated");
            this.breadcumb.label = this.make_label();
            this.$bvModal.msgBoxOk(this.object_name + " updated");
          });
      } else {
        document.querySelector("#editor-form").reportValidity();
      }
    },
    create() {
      if (document.querySelector("#editor-form").checkValidity()) {
        this.$store
          .dispatch(this.ressource + "/create", this.object)
          .then(data => {
            console.log(this.object_name + " created");
            this.$bvModal.msgBoxOk(this.object_name + " created");
            this.$router.push({
              name: this.$route.name,
              params: {
                id: data.id
              }
            });
          })
          .catch(error => {
            console.log(error.response);
          });
      } else {
        document.querySelector("#editor-form").reportValidity();
      }
    },
    destroy() {
      this.$store
        .dispatch(this.ressource + "/destroy", this.object.id)
        .then(() => {
          this.$router.push({
            name: this.ressource
          });
        });
    }
  },
  beforeMount() {
    this.initComponent().then(() => {
      this.initObject(this.$route);
    });
  },
  beforeRouteUpdate(to, from, next) {
    this.$store.dispatch(POP_BREADCUMB);
    this.initObject(to);
    next();
  },
  beforeRouteLeave(to, from, next) {
    this.$store.dispatch(POP_BREADCUMB);
    next();
  }
};
