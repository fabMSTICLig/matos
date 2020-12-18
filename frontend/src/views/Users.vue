<template>
  <div id="users">
    <Breadcumb />
    <router-view></router-view>
  </div>
</template>

<script>
import Breadcumb from "@/components/Breadcumb";
/*
  Routeur Vue Utilisateurs
*/
export default {
  name: "Users",
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
