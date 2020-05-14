<template>
  <div>
    <div class="input-group">
      <div class="input-group-prepend">
        <span class="input-group-text">Ajouter</span>
      </div>
      <input-datalist
        v-model="new_object_id"
        :ressource="ressource"
      ></input-datalist>
      <div class="input-group-append">
        <button class="btn btn-primary" type="button" @click="addObject">
          Valider
        </button>
      </div>
    </div>
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
        >
          X
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import InputDatalist from "@/components/InputDatalist";
export default {
  name: "DynList",
  props: {
    ressource: {
      type: String,
      required: true
    },
    value: {
      type: Array,
      required: true
    }
  },
  components: {
    InputDatalist
  },
  data() {
    return {
      new_object_id: 0
    };
  },
  computed: {
    objects_list() {
      return this.$store.getters[this.ressource + "/list"];
    },
    objects_filtered() {
      return this.objects_list.filter(item => {
        return this.value.indexOf(item.id) > -1;
      });
    }
  },
  methods: {
    addObject() {
      if (
        this.value.indexOf(this.new_object_id) == -1 &&
        this.objects_list.some(item => item.id == this.new_object_id)
      ) {
        this.value.push(this.new_object_id);
        this.$emit("input", this.value);
        this.new_object_id = 0;
      }
    },
    removeObject(id) {
      const index = this.value.indexOf(id);
      if (index > -1) {
        this.value.splice(index, 1);
        this.$emit("input", this.value);
      }
    }
  }
};
</script>
