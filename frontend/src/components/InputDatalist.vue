<template>
  <div class="form-control p-0">
    <multiselect
      v-model="item"
      :options="options"
      track-by="name"
      label="name"
      :searchable="true"
      :allow-empty="true"
      select-label=""
    ></multiselect>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  name: "input-datalist",
  props: {
    value: {
      type: null,
      required: true,
    },
    ressource: {
      type: [String, Array],
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
      activeDset: true,
      id: "",
      item: null,
    };
  },
  components: {
    Multiselect,
  },
  watch: {
    value: function (newval) {
      if (newval == 0) {
        this.activeDset = true;
        this.input_value = "";
      }
    },
    item() {
      this.$emit("input", this.item.value.id);
    },
  },
  computed: {
    objects_list() {
      if (typeof this.ressource == "string")
        return this.$store.getters[this.ressource + "/list"];
      else return this.ressource;
    },
    options() {
      /*
        Boucle sur les items de la liste
        Possibilité de désactiver un item en passant la clé $isDisabled en vérifiant une propriété active d'un item
        @see https://vue-multiselect.js.org/#sub-custom-option-template
      */
      let options = [];
      for (let i = 0; i <= this.objects_list.length - 1; i++) {
        let option = {
          value: this.objects_list[i],
          name: this.makeLabelOrName(this.objects_list[i]),
          $isDisabled: this.objects_list[i].borrowed ? true : false,
        };
        options.push(option);
      }
      return options;
    },

    inputValue: {
      get() {
        if (this.value) {
          var item = this.objects_list.find(
            (item) => item.id.toString() == this.value.toString()
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
          item = this.objects_list.find((item) => item.id.toString() == val);
        }
        if (item != undefined) {
          this.input_value = this.makeLabelOrName(item);
          this.activeDset = false;
          this.$emit("input", item.id);
        } else {
          this.activeDset = true;
          this.input_value = val;
        }
      },
    },
  },
  methods: {
    makeLabelOrName(item) {
      return this.makeLabel ? this.makeLabel(item) : item.name;
    },
  },
  beforeMount() {
    if (typeof this.ressource == "string")
      this.$store.dispatch(this.ressource + "/fetchList").then(() => {
        if (this.value && this.options) {
          let selected_item = this.options.filter((item) => {
            return item.value.id == this.value;
          });
          this.item = selected_item[0];
        }
      });
  },
  mounted() {
    this.id = String(this._uid);
  },
  created() {},
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
