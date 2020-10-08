<template>
  <ol class="breadcrumb">
    <router-link
      v-for="(item, index) in breaditems"
      :key="item.name"
      :to="{ name: item.name, params: item.params }"
      v-slot="{ href, route, navigate, isActive, isExactActive }"
    >
      <li class="breadcrumb-item" :class="[isExactActive && 'active']">
        <a v-if="!isExactActive" :href="href" @click="navigate">
          <span v-text="item.label"></span>
        </a>
        <span v-else v-text="item.label"></span>
      </li>
    </router-link>
  </ol>
</template>

<script>
export default {
  name: "Breadcumb",

  data() {
    return {
      breaditems: [],
      labelchild:""
    };
  },
  computed: {},
  methods: {
    updateItems(route) {
      var promises = [];
      route.matched.forEach(item => {
        this.makeBreadItem(item, route, promises);
      });
      Promise.all(promises).then(values => {
        this.breaditems = values;
      });
    },
    makeBreadItem(item, route, promises) {
      if ("breadcumb" in item.meta) {
        promises.push(
          new Promise(resolve => {
            if (typeof item.meta.breadcumb.label == "string") {
              resolve({
                label: item.meta.breadcumb.label,
                name: item.meta.breadcumb.name
              });
            } else {
              if (route.params[item.meta.routeparam] == "new") {
                resolve({
                  label: "Création",
                  name: item.meta.breadcumb.name,
                  params: route.params
                });
              } else {
                var prefix = "";
                if ("prefix" in item.meta.breadcumb.label) {
                  item.meta.breadcumb.label.prefix.forEach(item => {
                    prefix +=
                      item.ressource + "/" + route.params[item.param] + "/";
                  });
                }

                this.$store
                  .dispatch(
                    item.meta.breadcumb.label.ressource + "/fetchSingle",
                    { id: route.params[item.meta.routeparam], prefix: prefix }
                  )
                  .then(data => {
                    resolve({
                      label: data[item.meta.breadcumb.label.labelprop],
                      name: item.meta.breadcumb.name,
                      params: route.params
                    });
                  });
            }
          }
        })
      );
      }
      if(item.meta.breadcumb) {
        if(item.meta.breadcumb.label.labelchild)
          promises.push(
            new Promise(resolve => {
              resolve({
                label: item.meta.breadcumb.label.labelchild,
                name: ""
                });
              })
            );
        }
    }
  },
  watch: {
    $route(to) {
      this.updateItems(to);
    }
  },
  beforeMount() {
    this.updateItems(this.$route);
  }
};
</script>
