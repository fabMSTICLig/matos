<template>
  <div class="home">
    <data-policy></data-policy>
  </div>
</template>

<script>
// @ is an alias to /src
import DataPolicy from "./DataPolicy"

export default {
  name: "Home",
  components: {
    DataPolicy
  }
};
</script>
