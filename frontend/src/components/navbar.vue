<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-storm">
    <router-link
      tag="a"
      class="navbar-brand"
      class-active="active-manage"
      :to="items[0].link"
      v-if="items"
    >{{items[0].name}}</router-link>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li v-for="(item, index) in links" :key="index" class="nav-item">
          <router-link
            tag="a"
            class="nav-link"
            class-active="active-manage"
            :to="item.link"
          >{{item.name}}</router-link>
        </li>

        <li class="nav-item">
          <button class="btn btn-default">(-)</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'navbar',

  props: {
    items: {
      type: Array
    },
    entity: {
      type: Number
    }
  },

  computed: {
    links () {
      console.log(
        this.items.filter(function (pos, item) {
          return pos
        })
      )
      return this.items.filter(function (item, pos) {
        return pos > 0 ? item : ''
      })
    }
  }
}
</script>
