<template>
  <div class="home">
    <div class="container">
      <navbar :items="items"></navbar>

      <organization
        v-bind:organization="entity.id"
        v-show="isManagement"
      ></organization>
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

export default {
  name: "Manage",

  data() {
    return {
      organization: 1
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
      if (this.$route.name == "manage-entity") {
        console.log("chargement entité");
        this.organization = this.$route.params.id;
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
    ManageUsers
  },
  computed: {
    ...mapGetters(["equipments"]),

    ...mapState({
      organizations: state => state.organizations
    }),

    isUsersManagement() {
      return this.$route.name == "manage-users";
    },

    isManagement() {
      let re = /manage\-\w+/
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
        { link: "/manage", name: this.entity.name },
        { link: "/manage/users", name: "Utilisateurs" },
        { link: "lends", name: "Prêts en cours" },
        { link: "./history", name: "Historique de prêts" },
        { link: "./equipments", name: "Matériels" }
      ];
    }
  }
};
</script>
