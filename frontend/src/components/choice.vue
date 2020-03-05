<template>
<div class="self-container">
  <div class="row">
    <div class="col align-self-center">
      <b-button
        :class="visible ? null : 'collapsed'"
        :aria-expanded="visible ? 'true' : 'false'"
        aria-controls="`collapse-${title}`"
        @click="visible = !visible"
        variant="info"
      >{{ title}}</b-button>
    <b-collapse id="`collapse-${title}`" v-model="visible" class="mt-2">
      <b-card v-for="( item, index ) in items" :key="index">
          <router-link tag="a" class="link-submenu" class-active="active-manage" :to="item.link" v-if="item.link">{{item.name}}</router-link>
      </b-card>
    </b-collapse>
    </div>
  </div>
</div>
</template>

<script>
    export default {
  name: 'choice',
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
      type: Array,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: ''
      
    }
  },

  computed: {

   
  }
       
}
</script>
