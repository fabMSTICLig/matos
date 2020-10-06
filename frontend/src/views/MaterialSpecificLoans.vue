<template>
  <div>
    <div v-if="selected_object" class="col col-12">
      <div class="row">
        <div class="col-md-5">
          <div class="card">
            <div class="card-header">
              <div
                class="form-group d-inline-flex d-xl-flex flex-row flex-fill justify-content-between"
              >
                <h5 style="margin-top: 7px;">Instances</h5>
                <input type="text" class="border rounded-0" value="Search" />
                <button class="btn btn-primary" type="button">Ordre</button>
              </div>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Nom</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in objects_list" :key="item.id">
                      <td style="background: #eae5e5;">{{ item.name }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- pagination -->
            </div>
          </div>
        </div>
        <div class="col-md-7">
          <div class="card">
            <div class="card-header d-inline-flex justify-content-between">
              <h5 style="margin-top: 7px;">Prêts</h5>
              <div class="form-group d-inline-flex d-xl-flex flex-row">
                <input
                  type="text"
                  class="border rounded-0"
                  value="Search"
                /><button class="btn btn-primary" type="button">Valider</button>
              </div>
              <div class="form-group d-inline-flex d-xl-flex flex-row">
                <div class="dropdown">
                  <button
                    class="btn btn-light dropdown-toggle"
                    data-toggle="dropdown"
                    aria-expanded="false"
                    type="button"
                  >
                    Ordre
                  </button>
                  <div class="dropdown-menu">
                    <a class="dropdown-item" href="#">Entité</a
                    ><a class="dropdown-item" href="#">Status</a>
                  </div>
                </div>
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
                          <tr v-for="loan in loans" :key="loan.id">
                            <td>
                              {{ userById(loan.user) | field("username") }}
                            </td>
                            <td>{{ status[loan.status] }}</td>
                            <td>{{ loan.checkout_date }}</td>
                            <td>{{ loan.due_date }}</td>
                            <td>{{ loan.return_date }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
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

export default {
  name: "MaterialSpecificLoans",
  data() {
    return {
      selected_object: null,
      material: "",
      ressource: "entities/specificMaterials",
      sort_input: 1,
      sort_choices: {
        due_date: { value: 1, label: "Date retour prévue" },
        checkout_date: { value: 2, label: "Date sortie" }
      }
    };
  },

  computed: {
    ...mapGetters({
      loans: "entities/specificMaterials/instances/loans",
      status: "loans/status",
      userById: "users/byId",
      users: "users/list"
    }),
    objects_list() {
      return this.$store.getters["entities/specificMaterials/instances/list"];
    },
    instancePrefix() {
      return (
        "entities/" +
        this.$route.params.entityid +
        "/specificmaterials/" +
        this.$route.params.matid +
        "/"
      );
    },
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    }
  },
  methods: {
    selectObject(item) {
      this.selected_object = Object.assign({}, item);
    }
  },
  beforeMount() {
    this.$store.dispatch("users/fetchList");
    this.$store.dispatch("loans/fetchStatus");
    this.$store
      .dispatch(this.ressource + "/fetchSingle", {
        id: this.$route.params.matid,
        prefix: this.prefix
      })
      .then(data => {
        this.material = data;
      });

    this.$store
      .dispatch("entities/specificMaterials/instances/fetchList", {
        prefix: this.instancePrefix
      })
      .then(() => {
        if (this.objects_list.length > 0) {
          this.selectObject(this.objects_list[0]);
        }
      });
    this.$store
      .dispatch("entities/specificMaterials/instances/materialLoans", {
        id_entity: this.$route.params.entityid,
        id_specificmaterial: this.$route.params.matid,
        id_instance: "17"
      })
      .then(data => {
        console.log("prets materiel");
        console.log(data);
      });
  }
};
</script>
