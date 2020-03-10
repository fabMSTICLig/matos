<template>
  <div>
    <b-card-group columns>
      <ul>
        <li v-for="orga in orgas" :key="orga.id">{{ orga.name }}</li>
      </ul>
    </b-card-group>
  </div>
</template>

<script>
import ApiService from "@/common/api.service";
import { mapGetters } from "vuex";
import { FETCH_ORGAS } from "@/store/actions.type";


export default {
  name: "Admin",
  components: {},
  computed: {
    ...mapGetters(["orgas"])
  },
  methods: {},
  beforeMount() {
    this.$store.dispatch(FETCH_ORGAS);
  }
};
</script>
