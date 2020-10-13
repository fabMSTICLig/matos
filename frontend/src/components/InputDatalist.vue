<template>
  <div class="form-control p-0">
    <model-select :options="options"
                  v-model="item"
                  placeholder="Select"
                  v-if="objects_list.length"
                  :id=id>
    </model-select>
  </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select';

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
      id: "",
      item: {
        value: '',
        text: ''
      }
    };
  },
  components: {
    ModelSelect
  },
  watch: {
    value: function(newval) {
      if (newval == 0) {
        this.activeDset = true;
        this.input_value = "";
      }
    },
    item(){
      if(this.item.value)
        this.$emit("input", this.item.value.id);
    },
    options(opts){
      if(this.value && typeof this.value == "number")
        console.log(this.value);
        let self = this;
        this.item = opts.find(
          item => item.value.id.toString() == self.value
        );
        console.log(this.item);
      }
  },
  computed: {
    objects_list() {
      if (typeof this.ressource == "string")
        return this.$store.getters[this.ressource + "/list"];
      else return this.ressource;
    },
    options(){
      let options = [];
      for(let i=0; i<=this.objects_list.length-1; i++){
        let option = {
          value: this.objects_list[i],
          text: this.makeLabelOrName(this.objects_list[i])
        };
        options.push(option)
      }
      return options;
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
