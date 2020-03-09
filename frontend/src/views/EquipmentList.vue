<template>
  <div class="home">
    <hr />
    <h4 class="text-center font-weight-bold">Equipments liste</h4>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Title</th>
          <th scope="col">Quantité</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(equipment) in equipments" v-bind:key="equipment.id">
          <td>
            <router-link tag="a" :to="itemLink(equipment.id)">{{ equipment.title }}</router-link>
          </td>
          <td>{{ equipment.sku }}</td>

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
    },
     itemLink(index) {
      return "/equipment/"+index
    }

  },

  mounted() {
    this.$store.dispatch("fetchEquipments");
  },

  components: {
    Organization,
    
  },
  computed: {
    ...mapGetters(["equipments"]),

   
    
  }
};
</script>
