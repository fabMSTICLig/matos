<template>
  <div id="entities">
    <Breadcumb />
    <router-view></router-view>
  </div>
</template>

<script>
import Breadcumb from "@/components/Breadcumb";
/*
  Routeur Entités
*/
export default {
  name: "Entities",
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
