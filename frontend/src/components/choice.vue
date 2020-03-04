<template>
<div>
 <b-button v-b-toggle.collapse-1 variant="primary">{{title}}</b-button>
  <b-collapse id="collapse-1" class="mt-2">
    <b-card v-for="( item, index ) in items" :key="index">
        <router-link tag="a" class="nav-link" class-active="active-manage" :to="item.link">{{item.name}}</router-link>
    </b-card>
  </b-collapse>
</div>
</template>

<script>
    export default {
  name: 'choice',

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
