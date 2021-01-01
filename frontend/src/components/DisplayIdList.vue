<template>
  <ul class="list-group list-group-horizontal d-flew flex-wrap">
    <li
      class="list-group-item border rounded"
      v-for="item in objects_filtered"
      :key="item.id"
    >
      {{ item.name }}
    </li>
  </ul>
</template>

<script>
/*
    Component used to display items in list
    props ressource store, object and field to display
  */
export default {
  name: "DisplayIdList",
  props: {
    ressource: {
      type: String,
      required: true
    },
    object: {
      type: Object,
      required: true
    },
    fieldName: {
      type: String,
      required: true
    },
    autoload: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    objects_list() {
      return this.$store.getters[this.ressource + "/list"];
    },
    objects_filtered() {
      return this.objects_list.filter(item => {
        return this.object[this.fieldName].includes(item.id);
      });
    }
  },
  methods: {},
  beforeMount() {
    if (this.autoload) this.$store.dispatch(this.ressource + "/fetchList");
  }
};
</script>
