<template>
  <div>
    <div v-if="!readonly" :id="_uid">
      <div class="input-group" style="height:43px;">
        <!--<div class="input-group-prepend">
          <span class="input-group-text">Ajouter</span>
        </div>-->
        <multiselect
          :value="valueIntern"
          :options="optionsIntern"
          :multiple="true"
          track-by="id"
          :custom-label="makeLabel"
          label="name"
          hide-selected
          placeholder="Pick a value"
          :reset-after="true"
          @select="addObject"
          ><template slot="tag"><span></span></template>
        </multiselect>
      </div>
    </div>
    <ul class="list-group">
      <li
        class="list-group-item d-flex justify-content-between align-items-center"
        v-for="item in valueIntern"
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
          @click="removeObject(item)"
          v-if="!readonly"
        >
          X
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
/*
  Component mixing list input and list group items
*/
export default {
  name: "DynList",
  props: {
    options: {
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
    Multiselect
  },
  data() {
    return {};
  },
  computed: {
    optionsIntern() {
      if (typeof this.options == "string")
        return this.$store.getters[this.options + "/list"];
      else return this.options;
    },
    valueIntern() {
      return this.optionsIntern.filter(el => this.value.includes(el.id));
    }
  },
  methods: {
    addObject(item) {
      this.$emit("input", [item.id].concat(this.value));
    },
    removeObject(item) {
      const index = this.value.indexOf(item.id);
      if (index > -1) {
        let ret = [];
        ret = ret.concat(this.value);
        ret.splice(index, 1);
        this.$emit("input", ret);
      }
    }
  },
  beforeMount() {
    if (typeof this.options == "string")
      this.$store.dispatch(this.options + "/fetchList");
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
