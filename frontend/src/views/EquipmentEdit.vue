<template>
  <form action="" @submit="updateEquipment(equipment)" v-if="equipment">
    <h4 class="text-center font-weight-bold">Equipment creation form</h4>
    <div class="form-group">
      <input
        type="text"
        placeholder="Post title"
        v-model="equipment.title"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <input
        type="text"
        v-model="equipment.sku"
        placeholder="Equipment stock"
        class="form-control"
      />
    </div>
    <div class="form-group">
      <input
        type="text"
        v-model="equipment.barcode"
        placeholder="Equipment barcode"
        class="form-control"
      />
    </div>
    <div class="form-group">
      <textarea
        v-model="equipment.description"
        placeholder="Description"
        class="form-control"
      />
    </div>
    <div class="form-group">
      <input
        type="number"
        v-model="equipment.location"
        placeholder="Organisation"
        class="form-control"
      />
    </div>
    <div class="form-group">
      {{equipment.families}}
      <categorie
        v-if="equipment.families"
        v-model="equipment.families"
      ></categorie>
      </div>
    <div class="form-group">
      <button
        class="btn btn-block btn-primary"
        @click.prevent="updateEquipment(equipment)"
      >
        Submit
      </button>
    </div>
  </form>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import categorie from "./Categorie.vue";

export default {
  name: "EquipmentEdit",
  data() {
    return {
      organisation: "",
      categorie: ""
    };
  },
  methods: {
    /**findEquipment () {
      console.log(this.equipments)
      this.equipment = this.equipments.find(equipment => {
        // eslint-disable-next-line eqeqeq
        return equipment.id == this.$route.params.id
      })
    },**/
    updateEquipment(equipment) {
      console.log(this.equipment)
      this.$store.dispatch("updateEquipment", equipment);
    }
  },
  mounted() {
    this.$store.dispatch("fetchEquipments");
  },
  components: {
    categorie
  },
  computed: {
    equipment() {
      console.log("equipement");
      return (
        this.equipments.find(
          equipement => equipement.id == this.$route.params.id
        ) || {}
      );
    },
    ...mapGetters(["equipments"]),
    ...mapState({
      equipments: state => state.equipments
    })
  }
};
</script>

<style scoped></style>
