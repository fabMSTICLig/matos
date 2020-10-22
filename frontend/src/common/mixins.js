import Pagination from "@/components/Pagination";
import { showMsgOk } from "@/components/Modal";

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
  computed: {
    prefix() {
      return "";
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
      this.$store
        .dispatch(this.ressource + "/fetchList", { prefix: this.prefix })
        .then(() => {
          if (this.objects_filtered.length > 0) {
            this.selected_object = this.objects_filtered[0];
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

export const MaterialAvailability = {
  methods: {
    getMaterialAvailability(pending_loan) {
      let self = this;

      Object.keys(this.specificinstances).map(function(objectKey) {
        var instances = self.specificinstances[objectKey];
        var instances_notin = [];
        pending_loan.specific_materials.some(function(a) {
          if (!instances.indexOf(a.id)) {
            instances_notin.push(a);
            return true;
          }
        });

        instances.forEach(item => {
          self.$store
            .dispatch("entities/specificMaterials/instances/materialLoans", {
              id_entity: pending_loan.entity,
              id_specificmaterial: item.model,
              id_instance: item.id
            })
            .then(data => {
              var borrowed = data.filter(loan => {
                if (pending_loan.id) {
                  if (loan.id !== pending_loan.id) {
                    return self.filterBorrowed(loan,pending_loan);
                  }
                } else {
                  return self.filterBorrowed(loan, pending_loan);
                }
              });
              if (borrowed.length) {
                console.log("borrowed");
                let instance_borrowed = instances.find(i => i.id == item.id);
                var spec_instances = self.specificinstances[item.model].find(
                  i => i.id == instance_borrowed.id
                );
                self.$set(spec_instances, "borrowed", true);
                console.log(self.specificinstances);
              }
              if (!borrowed.length) {
                self.specificinstances[item.model].forEach(item => {
                  self.$set(item, "borrowed", "");
                });
              }
          });
        });
      });
    },
    filterBorrowed(loan, pending_loan) {
      return loan.status == 3
        ? (loan.due_date > pending_loan.checkout_date &&
            loan.checkout_date <= pending_loan.checkout_date) ||
            (loan.return_date > pending_loan.checkout_date &&
              loan.checkout_date <= pending_loan.checkout_date) ||
            (loan.checkout_date >= pending_loan.checkout_date &&
              pending_loan.due_date > loan.checkout_date &&
              (pending_loan.return_date ? pending_loan.return_date.length==0 : false || !pending_loan.return_date)
            ) ||
            (pending_loan.return_date ? loan.checkout_date >= pending_loan.checkout_date &&
                loan.due_date > pending_loan.checkout_date &&
                pending_loan.return_date > loan.checkout_date : false)
        : false;
    }
  }
};
