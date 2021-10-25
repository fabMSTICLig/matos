<template>
  <div id="tags">
    <Breadcumb />
    <router-view></router-view>
  </div>
</template>

<script>
import Breadcumb from "@/components/Breadcumb";
/*
  Routeur Tags
*/
export default {
  name: "Tags",
  components: {
    Breadcumb,
  },
  data() {
    return {};
  },

  computed: {},
  methods: {},
};
</script>
