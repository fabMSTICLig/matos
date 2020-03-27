<template>
  <div>
    <div role="tablist">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button
            :class="visible ? null : 'collapsed'"
            :aria-expanded="visible ? 'true' : 'false'"
            aria-controls="setId(items.title)"
          >+</b-button>
        </b-card-header>
        <b-collapse
          id="setId(items.title)"
          v-model="visible"
          accordion="my-accordion"
          role="tabpanel"
        >
          <b-card-body>
            <b-card-text v-for="item in items" :key="item.id">{{item.title}}</b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'accordion',
  data () {
    return {
      visible: false
    }
  },
  props: {
    title: {
      type: String,
      default: 'toggle'
    },
    items: {
      type: Array
    }
  },
  methods: {
    setId (title) {
      return `accordion-${title}`
    }
  },

  computed: {}
}
</script>
