<template>
  <div class="home">
    <hr />
    <h4 class="text-center font-weight-bold">Réservation</h4>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Organization from "./Organization.vue";

export default {
  name: "Home",

  
  components: {
    Organization,
    
  }
  
};
</script>
