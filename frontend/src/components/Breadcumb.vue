<template>
  <ol class="breadcrumb">
    <router-link v-for="(item, index) in breadcumb_list" :key="item.url"
      :to="item.url"
      v-slot="{ href, route, navigate, isActive, isExactActive }"
      >
        <li class="breadcrumb-item" :class="[isExactActive && 'active']" >
            <a v-if="!isExactActive" :href="href" @click="navigate">
                <span v-text="item.label"></span>
            </a>
            <span v-else v-text="item.label"></span>
        </li>
    </router-link>
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
