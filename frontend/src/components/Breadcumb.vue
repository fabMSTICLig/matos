<template>
  <ol class="breadcrumb">
    <li class="breadcrumb-item" v-for="item in breadcumb_list" :key="item.url">
      <router-link :to="item.url"
        ><span v-text="item.label"></span
      ></router-link>
    </li>
  </ol>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Breadcumb",

  computed: {
    ...mapGetters(["breadcumb_list"])
  },
  methods: {}
};
</script>
