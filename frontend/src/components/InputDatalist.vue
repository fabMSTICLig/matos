<template>
  <div class="form-control p-0">
    <input class="h-100 w-100" type="text" :list="_uid" v-model="inputValue" />
    <datalist :id="_uid" v-if="activeDset">
      <option
        v-for="item in objects_list"
        :key="item.id"
        :value="item.id"
        v-text="makeLabelOrName(item)"
      ></option>
    </datalist>
  </div>
</template>

<script>
export default {
  name: "input-datalist",
  props: {
    value: {
      type: null,
      required: true
    },
    ressource: {
      type: [String, Array],
      required: true
    },
    makeLabel: {
      type: Function,
      required: false
    }
  },
  data() {
    return {
      input_value: "",
      activeDset: true,
      id: ""
    };
  },
  watch: {
    value: function(newval) {
      if (newval == 0) {
        this.activeDset = true;
        this.input_value = "";
      }
    }
  },
  computed: {
    objects_list() {
      if (typeof this.ressource == "string")
        return this.$store.getters[this.ressource + "/list"];
      else return this.ressource;
    },

    inputValue: {
      get() {
        if (this.value) {
          var item = this.objects_list.find(
            item => item.id.toString() == this.value.toString()
          );
        }
        if (item != undefined) {
          return this.makeLabelOrName(item);
        } else {
          return this.input_value;
        }
      },
      set(val) {
        var item = undefined;
        if (Number(val)) {
          item = this.objects_list.find(item => item.id.toString() == val);
        }
        if (item != undefined) {
          this.input_value = this.makeLabelOrName(item);
          this.activeDset = false;
          this.$emit("input", item.id);
        } else {
          this.activeDset = true;
          this.input_value = val;
        }
      }
    }
  },
  methods: {
    makeLabelOrName(item) {
      return this.makeLabel ? this.makeLabel(item) : item.name;
    }
  },
  beforeMount() {
    if (typeof this.ressource == "string")
      this.$store.dispatch(this.ressource + "/fetchList");
  },
  mounted() {
    this.id = String(this._uid);
  }
};
</script>
