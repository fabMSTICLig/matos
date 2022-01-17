<template>
  <div>
    <div v-if="!readonly">
      <div
        class="input-group"
        style="height: 43px"
      >
        <Multiselect
          ref="mtselect"
          :model-value="valuesIntern"
          track-by="id"
          label="name"
          mode="multiple"
          :options="fetchOptions"
          :close-on-select="false"
          :filter-results="isArray"
          :min-chars="0"
          :resolve-on-load="isArray"
          :delay="1"
          :searchable="true"
          :multiple-label="multipleLabel"
          no-options-text="Veuillez entrer des charactères"
          :hide-selected="true"
          :can-clear="false"
          open-direction="top"
          @change="change"
        />
      </div>
    </div>
    <ul class="list-group">
      <li
        v-for="item in valuesIntern"
        :key="item.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>
          <slot :item="item">
            {{ item.name }}
          </slot>
        </span>
        <button
          v-if="!readonly"
          class="btn btn-danger"
          type="button"
          @click="removeItem(item)"
        >
          X
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeMount, defineProps, defineEmits } from "vue";
import { useStore } from "vuex";

import Multiselect from "@vueform/multiselect";

const store = useStore();

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  ressource: {
    type: [String, Array],
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  makeLabel: {
    type: Function,
    default: (o) => o.name,
  },
  readonly: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const mtselect = ref();

const valuesLoadBuffer = ref([])

const valuesIntern = computed(()=>{
  if (isArray.value)
    return props.ressource.filter(
      (o) => props.modelValue.includes(o.id)
    );
    else{
      return valuesLoadBuffer.value
    }
});
const isArray = computed(() => Array.isArray(props.ressource));
onBeforeMount(async () => {
  if (!isArray.value)
    store
      .dispatch(props.ressource + "/fetchList", {
        params: { ids: props.modelValue.join(",") },
      })
      .then((data) => {
        data.forEach((o) =>
          mtselect.value.select({ value: o, name: props.makeLabel(o) })
        );
      });
});

function multipleLabel() {
  return "";
}

async function fetchOptions(query) {
  let data = [];
  if (Array.isArray(props.ressource)) data = props.ressource;
  else {
    data = await store.dispatch(props.ressource + "/fetchList", {
      params: { search: query },
    });
  }
  return data
    .filter((o) => !props.modelValue.includes(o.id))
    .map((o) => {
      return {
        name: props.makeLabel(o),
        value: o,
        disabled: false,
      };
    });
}

function change(v) {
  if(!isArray.value)
    valuesLoadBuffer.value=v
  emit(
    "update:modelValue",
    v.map((o) => o.id)
  );
}

function removeItem(item) {
  mtselect.value.remove({ value: item });
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
