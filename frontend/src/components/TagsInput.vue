<template>
  <ul class="list-group list-group-horizontal d-flew flex-wrap">
    <li
      class="list-group-item border rounded"
      v-for="item in objects_filtered"
      :key="item.id"
    >
      <span> {{ item.name }}</span>
      <button
        type="button"
        class="btn btn-danger btn-sm ml-1"
        v-on:click="removeTag(item)"
      >
        X
      </button>
    </li>
    <input
      type="text"
      class="form-control"
      :list="_uid"
      v-model="inputValue"
      placeholder="Ajouter"
      @keyup.enter="addTag"
      @change="addTag"
    />
    <datalist :id="_uid" v-if="activeDset">
      <option
        v-for="item in objects_datalist"
        :key="item.id"
        :value="item.name"
        v-text="item.name"
      ></option>
    </datalist>
  </ul>
</template>

<script>
/*
    Tags Input for saving tags
  */
export default {
  name: "TagsInput",
  props: {
    ressource: {
      type: String,
      required: true,
    },
    list: {
      type: Array,
      required: true,
    },
    forbidAdd: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      input_value: "",
      activeDset: true,
    };
  },
  computed: {
    objects_list() {
      return this.$store.getters[this.ressource + "/list"];
    },
    objects_filtered() {
      return this.objects_list.filter((item) => {
        return this.list.includes(item.id);
      });
    },
    objects_datalist() {
      return this.objects_list.filter((item) => {
        return !this.list.includes(item.id);
      });
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
    addTag() {
      if (this.input_value == "") return;
      var tag = this.objects_datalist.find(
        (item) => item.name == this.input_value
      );
      if (tag) {
        this.$emit("add", tag.id);
        this.input_value = "";
      } else if (!this.forbidAdd) {
        tag = this.objects_filtered.find(
          (item) => item.name == this.input_value
        );
        if (tag) this.input_value = "";
        else {
          this.$store
            .dispatch(this.ressource + "/create", {
              data: { name: this.input_value },
            })
            .then((data) => {
              // eslint-disable-next-line
              console.log("Tag created");
              this.$emit("add", data.id);
              this.input_value = "";
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.log(JSON.stringify(error));
            });
        }
      }
    },
    removeTag(tag) {
      this.$emit("remove", tag.id);
    },
  },
  beforeMount() {
    this.$store.dispatch(this.ressource + "/fetchList");
  },
};
</script>
