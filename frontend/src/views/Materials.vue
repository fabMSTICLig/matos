<template>
  <div>
    <h2>{{ name }}</h2>

    <router-view></router-view>
  </div>
</template>

<script>
/*
    Router vue matériels
  */
export default {
  name: "Materials",
  components: {},
  computed: {
    name() {
      var entity = this.$store.getters["entities/byId"](
        this.$route.params.entityid
      );
      if (entity) {
        return entity.name;
      } else return "";
    },
  },
};
</script>
