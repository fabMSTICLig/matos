<template>
  <div>
    <div class="col col-12">
      <div class="row">
        <div class="col col-8">
          <div class="card">
            <div class="card-header d-inline-flex justify-content-between">
              <h5 style="margin-top: 7px;">Prêts</h5>
              <div class="form-group d-inline-flex d-xl-flex flex-row">
                <input type="text" class="border rounded-0" value="Search" />
                <button class="btn btn-primary" type="button">Valider</button>
              </div>
              <div class="form-group d-inline-flex d-xl-flex flex-row">
                <label class="mr-1">Ordre : </label>
                <select class="form-control" v-model="sort_input">
                  <option
                    v-for="item in sort_choices"
                    :value="item.value"
                    :key="item.value"
                    >{{ item.label }}</option
                  >
                </select>
              </div>
              <div class="form-group d-inline-flex d-xl-flex flex-row">
                <button class="btn btn-primary">Retour</button>
              </div>
            </div>
            <div class="card-body">
              <form>
                <div class="form-row">
                  <div class="col">
                    <div class="table-responsive d-table">
                      <table class="table">
                        <thead>
                          <tr>
                            <th>Utilisateur</th>
                            <th>Status</th>
                            <th>Date de sortie</th>
                            <th>Date de retour prévue</th>
                            <th>Date de retour</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="item in loans"
                            :key="item.id"
                            v-on:click="selected_object = item"
                            :class="{
                              'table-active':
                                selected_object && item.id == selected_object.id
                            }"
                          >
                            <td>
                              {{ userById(item.user) | field("username") }}
                            </td>
                            <td>{{ status[item.status] }}</td>
                            <td>{{ item.checkout_date }}</td>
                            <td>{{ item.due_date }}</td>
                            <td>{{ item.return_date }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <pagination
                      :total-pages="pages_count"
                      :total="objects_filtered.length"
                      :per-page="10"
                      :current-page="current_page"
                      @pagechanged="onPageChange"
                    />
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { ListMixin } from "@/common/mixins";

export default {
  name: "MaterialGenericLoans",
  mixins: [ListMixin],
  data() {
    return {
      selected_object: null,
      material: "",
      ressource: "entities/genericMaterials",
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" }
      }
    };
  },

  computed: {
    ...mapGetters({
      loans: "entities/genericMaterials/loans",
      status: "loans/status",
      userById: "users/byId"
    }),
    objects_filtered() {
      if (this.loans.length) {
        var filtered = this.loans.filter(item => {
          var user = this.userById(item.user);
          if (user)
            return (
              user.username
                .toLowerCase()
                .indexOf(this.search_input.toLowerCase()) > -1
            );
          else return true;
        });
        return filtered.sort((a, b) => {
          if (a.return_date && !b.return_date) return 1;
          if (b.return_date && !a.return_date) return -1;
          if (this.sort_input == this.sort_choices.due_date.value)
            return a.due_date.localeCompare(b.due_date);
          if (this.sort_input == this.sort_choices.checkout_date.value)
            return a.due_date.localeCompare(b.checkout_date);
        });
      }
      return this.loans;
    },
    instancePrefix() {
      return (
        "entities/" +
        this.$route.params.entityid +
        "/genericmaterials/" +
        this.$route.params.matid +
        "/"
      );
    },
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    }
  },
  methods: {},
  beforeMount() {
    this.$store.dispatch("loans/fetchStatus");
    this.$store.dispatch("users/fetchList");
    this.$store
      .dispatch(this.ressource + "/fetchSingle", {
        id: this.$route.params.matid,
        prefix: this.prefix
      })
      .then(data => {
        this.material = data;
      });

    this.$store
      .dispatch("entities/genericMaterials/getLoans", {
        id_entity: this.$route.params.entityid,
        id_genericmaterial: this.$route.params.matid
      })
      .then(data => {
        console.log("prets materiel");
        console.log(data);
      });
  }
};
</script>
