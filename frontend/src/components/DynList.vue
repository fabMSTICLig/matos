<template>
  <div>
    <form v-if="!readonly" :id="_uid" @submit="addObject">
      <div :class="show ? 'dropdown show' : 'dropdown'" @focusout="hide">
        <a
        :class="classtoogle + ' btn dropdown-toggle'"
        :id="'button' + _uid"
        @click="toogle">
          Ajouter
        </a>
        <div
            :class="show ? 'dropdown-menu show' : 'dropdown-menu'"
            :id="'tooltip' + _uid"
            v-if="objects_list"
          >
          <ul>
            <li v-for="item in objects_list" 
            :key="item.id"
            @click="addObject(item)"
            class="dropdown-item">
              <span>
                <slot v-bind:item="item">
                  {{ item.name }}
                </slot>
              </span>           
            </li>
          </ul>
        </div>
      </div>
    </form>
    <ul class="list-group">
      <li
        class="list-group-item d-flex justify-content-between align-items-center"
        v-for="item in objects_filtered"
        :key="item.id"
      >
        <span>
          <slot v-bind:item="item">
            {{ item.name }}
          </slot>
        </span>
        <button
          class="btn btn-danger"
          type="button"
          @click="removeObject(item.id)"
          v-if="!readonly"
        >
          X
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "DynList",
  props: {
    ressource: {
      type: [String, Array],
      required: true
    },
    value: {
      type: Array,
      required: true
    },
    makeLabel: {
      type: Function,
      required: false
    },
    readonly: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  components: {
  },
  data() {
    return {
      new_object_id: 0,
      items: [],
      show: false,
      classtoogle: 'btn-primary'
    };
  },
  computed: {
    objects_list() {
      if (typeof this.ressource == "string")
        return this.$store.getters[this.ressource + "/list"];
      else return this.ressource;
    },
    objects_filtered() {
      return this.objects_list.filter(item => {
        return this.value.indexOf(item.id) > -1;
      });
    },

  },
  methods: {
    toogle(e) {
      e.preventDefault();
      this.show = !this.show;
    },
    hide(e) {
      if (!this.$el.contains(e.relatedTarget)) {
        this.show = false;
      }
    },
    addObject(item) {
      //e.preventDefault();
      if (this.value.indexOf(item.id) > -1) {
        //this.new_object_id = 0;
      } else if (
        this.value.indexOf(item.id) == -1 &&
        this.objects_list.some(object => object.id == item.id)
      ) {
        this.value.push(item.id);
        this.$emit("input", this.value);
        //this.new_object_id = 0;
      }
      this.show = !this.show;
    },
    removeObject(id) {
      const index = this.value.indexOf(id);
      if (index > -1) {
        this.value.splice(index, 1);
        this.$emit("input", this.value);
      }
    },
    itemSelected(item) {
      let selected;
      let object_selected = this.value.filter(object => {
        console.log(object)
        if(item.id == object) {
          return true;
        }
      });

      if(object_selected.length) {
        selected = true
      }
      return selected;
    },
    makeLabelOrName(item) {
      return this.makeLabel ? this.makeLabel(item) : item.name;
    }
  },
  beforeMount() {
    //do something before mounting vue instance
    this.items = this.value
    if (typeof this.ressource == "string")
      this.$store.dispatch(this.ressource + "/fetchList");
      console.log(this.ressource)
  }
};
</script>
<style scoped>
.dropdown-menu.show > ul {
  margin-left: -40px;
}

.dropdown-menu.show  > ul > li:hover {
  cursor:pointer
}

.dropdown-toggle {
  color: #FFF;
}
</style>
