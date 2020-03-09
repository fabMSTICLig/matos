<template>
  <div class="home">
    <div class="container">
      <navbar :items="items" :entity="entity.id"></navbar>

      <organization
        v-bind:organization="entity.id"
        v-show="isManagement"
      ></organization>
      <equipment-list v-show="equipmentvue"></equipment-list>
      <manage-users v-show="isUsersManagement"></manage-users>
    </div>
    <hr />
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Organization from "./Organization.vue";
import ManageUsers from "./ManageUsers.vue";
import navbar from "@/components/navbar.vue";
import EquipmentList from "./EquipmentList.vue";

export default {
  name: "Manage",

  data() {
    return {
      organization: 1,
      equipmentvue: false,
      loansvue: false,
      usersvue: false,
      historyvue: false
    };
  },
  methods: {
    deleteEquipment(equipment) {
      this.$store.dispatch("deleteEquipment", equipment);
    }
  },

  mounted() {
    this.$store.dispatch("fetchEquipments");
  },
  watch: {
    $route(to, from) {
      this.show = false;
      console.log(to)
      if (this.$route.name == "manageEntity") {
        console.log("chargement entité");
        this.organization = this.$route.params.id;
        this.equipmentvue = false
        this.loansvue = false
        this.historyvue = false
        this.usersvue = false
      }
       if (this.$route.name == "manageEquipment-list") {
        console.log("liste equipements");
        this.equipmentvue = !this.equipmentvue;
      }
      if (this.$route.name !== "manageEquipment-list") {
        //this.equipmentvue = false;

      }
    }
  },

  created() {
    this.$store.dispatch("getOrganizations");
    console.log("route");
    console.log(this.$route.name);
  },

  components: {
    Organization,
    navbar,
    ManageUsers,
    EquipmentList,
  },
  computed: {
    ...mapGetters(["equipments"]),

    ...mapState({
      organizations: state => state.organizations
    }),

    isUsersManagement() {
      return this.$route.name == "manageUsers";
    },

    isManagement() {
      let re = /manageEntity/
      let myRoute = this.$route.name.match(re);
      let routeBase = "manage"
      if(myRoute && myRoute.length || this.$route.name == routeBase ) {
        return true
      }
    },

    entity() {
      console.log("entity default")
      console.log(this.organization)
      return (
        this.organizations.find(
          organization => organization.id == this.organization
        ) || {}
      );
    },

    items() {
      return [
        { link: "/manage/entity/"+this.entity.id, name: this.entity.name },
        { link: "/manage/users", name: "Utilisateurs" },
        { link: "lends", name: "Prêts en cours" },
        { link: "./history", name: "Historique de prêts" },
        { link: "/manage/entity/"+ this.$route.params.id + "/equipment-list", name: "Matériels" }
      ];
    }
  }
};
</script>
