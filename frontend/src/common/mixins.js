import Pagination from "@/components/Pagination";
import { showMsgOk } from "@/components/Modal";
/*
  Mixins pour liste et édition d'objets
  https://vuejs.org/v2/guide/mixins.html
*/
export const ListMixin = {
  components: {
    Pagination
  },

  data: function() {
    return {
      ressource: "",
      search_input: "",
      current_page: 1,
      selected_object: null
    };
  },
  watch: {
    search_change() {
      this.current_page = 1;
    }
  },
  computed: {
    prefix() {
      return "";
    },
    search_change() {
      return this.search_input;
    },
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
    },
    per_page() {
      return parseInt(process.env.VUE_APP_MAXLIST);
    }
  },
  methods: {
    onPageChange(page) {
      this.current_page = page;
    },
    initList() {
      return this.$store
        .dispatch(this.ressource + "/fetchList", { prefix: this.prefix })
        .then(() => {
          if (this.objects_filtered.length > 0) {
            this.selected_object = this.objects_filtered[0];
          }
          return Promise.resolve();
        });
    },
    initComponent() {
      return Promise.resolve();
    },
    listInitiated() {}
  },
  beforeMount() {
    this.initComponent().then(() => {
      let retinit = this.initList();
      if (retinit) retinit.then(() => this.listInitiated());
    });
  }
};

export const EditMixin = {
  data() {
    return {
      ressource: "",
      object: null,
      new_label: "",
      object_name: ""
    };
  },
  computed: {
    prefix() {
      return "";
    },
    is_new() {
      return this.$route.params[this.$route.meta.routeparam] == "new";
    },
    cardName() {
      return this.is_new ? this.new_label : this.make_label();
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
      if (route.params[route.meta.routeparam] == "new") {
        this.object = this.get_empty();
      } else if (parseInt(route.params[route.meta.routeparam], -1) != -1) {
        this.$store
          .dispatch(this.ressource + "/fetchSingle", {
            id: route.params[route.meta.routeparam],
            prefix: this.prefix
          })
          .then(data => {
            this.object = Object.assign({}, data);
          });
      }
    },
    update(msg) {
      if (document.querySelector("#editor-form").checkValidity()) {
        this.$store
          .dispatch(this.ressource + "/update", {
            id: this.object.id,
            data: this.object,
            prefix: this.prefix
          })
          .then(data => {
            this.object = Object.assign({}, data);
            // eslint-disable-next-line
            console.log(this.object_name + " updated");
            showMsgOk(this.object_name + " " + msg);
          });
      } else {
        document.querySelector("#editor-form").reportValidity();
      }
    },
    create() {
      if (document.querySelector("#editor-form").checkValidity()) {
        this.$store
          .dispatch(this.ressource + "/create", {
            data: this.object,
            prefix: this.prefix
          })
          .then(data => {
            // eslint-disable-next-line
            console.log(this.object_name + " created");
            showMsgOk(this.object_name + " created");
            var params = this.$route.params;
            params[this.$route.meta.routeparam] = data.id;
            this.$router.push({
              name: this.$route.name,
              params: params
            });
          })
          .catch(error => {
            // eslint-disable-next-line
            console.log(JSON.stringify(error));
          });
      } else {
        document.querySelector("#editor-form").reportValidity();
      }
    },
    destroy() {
      this.$store
        .dispatch(this.ressource + "/destroy", {
          id: this.object.id,
          prefix: this.prefix
        })
        .then(() => {
          this.$router.push({
            name: this.$route.meta.routedelete
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
    this.initComponent().then(() => {
      this.initObject(to);
      next();
    });
  }
};
