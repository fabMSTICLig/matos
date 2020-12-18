<template>
  <div id="affiliations">
    <Breadcumb />
    <router-view></router-view>
  </div>
</template>

<script>
import Breadcumb from "@/components/Breadcumb";
/*
  Vue Affiliations
*/
export default {
  name: "Affiliations",
  components: {
    Breadcumb
  },
  data() {
    return {};
  },

  computed: {},
  methods: {}
};
</script>
