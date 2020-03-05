<template>
  <div class="home">
    <hr />
    <h4 class="text-center font-weight-bold">Equipments liste</h4>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Title</th>
          <th scope="col">Quantité</th>
          <th scope="col">Categorie</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(equipment, index) in equipments" v-bind:key="equipment.id">
          <td>{{ equipment.title }}</td>
          <td>{{ equipment.sku }}</td>
          <td>
                <b-button v-b-toggle="'my-collapse-'+equipment.id">
                            <span>+</span>
                </b-button>
              <b-collapse :id="`my-collapse-${equipment.id}`">
                  <b-list-group>
                    <b-list-group-item v-for="item in equipment.family" :key="item.id">
                        <div>
                            {{item.title}}
                        </div>
                  </b-list-group-item>
              </b-list-group>
             </b-collapse>

          </td>

          <td>
            <button class="btn btn-danger" @click="deleteEquipment(equipment)">
              <b-icon-trash></b-icon-trash>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Organization from "./Organization.vue";

export default {
  name: "EquipmentList",

  methods: {
    deleteEquipment(equipment) {
      this.$store.dispatch("deleteEquipment", equipment);
    },
    idList(index) {
      return String(index)
    }
  },

  mounted() {
    this.$store.dispatch("fetchEquipments");
  },

  components: {
    Organization,
    
  },
  computed: {
    ...mapGetters(["equipments"])

    
  }
};
</script>
