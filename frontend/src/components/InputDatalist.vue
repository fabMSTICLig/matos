<template>
<div class="form-control p-0">
  <input class="h-100 w-100" type="text" :list="_uid" v-model="inputValue" >
  <datalist :id="_uid" v-if="activeDset">
      <option v-for="item in objects_list" :key="item.id" :value="item.id" v-text="makeLabelOrName(item)" ></option>
  </datalist>
</div>

</template>

<script>
export default {
  name: 'input-datalist',
  props: {
    value: {
      type: [String, Number],
      required: true,
    },
    ressource: {
      type: String,
      required: true,
    },
    makeLabel: {
      type: Function,
      required: false,
    },

  },
  data() {
    return {
      input_value: "",
      activeDset:true,
    }
  },
  computed: {
    objects_list() {
      return this.$store.getters[this.ressource + '/list']
    },

    inputValue: {
      get() {
        if(this.value==0)
        {
            this.activeDset=true;
            this.input_value=""
            return ""
        }
        var item = this.objects_list.find(item => item.id.toString() == this.value.toString())
        if (item != undefined) {
          return this.makeLabelOrName(item)
        } else {
            this.activeDset=true;
          return this.input_value;
        }
      },
      set(val) {
        var item = undefined
        if (Number(val)) {
          item = this.objects_list.find(item => item.id.toString() == val);
        }
        if (item != undefined) {
          this.input_value = this.makeLabelOrName(item)
          this.activeDset=false;
          this.$emit('input', item.id)
        } else {
          this.activeDset=true;
          this.input_value = val;
        }
      }
    },
  },
  methods:{
    makeLabelOrName(item){
        return this.makeLabel ? this.makeLabel(item) : item.name
    }
  },
  beforeMount() {
    this.$store.dispatch(this.ressource + '/fetchList')
  }
}
</script>
