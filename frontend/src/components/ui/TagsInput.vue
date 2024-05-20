<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <Multiselect
    ref="input"
    :model-value="modelValue"
    mode="tags"
    :close-on-select="false"
    :searchable="true"
    :create-option="!forbidAdd"
    :append-new-option="false"
    :append-new-tag="false"
    :options="options"
    @option="addOption"
    @deselect="removeOption"
    @change="change"
  />
</template>
<script setup>
import { ref, computed } from "vue";
import Multiselect from "@vueform/multiselect";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  ressource: {
    type : Array,
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  create:{
    type: Function,
    default: ()=>{},
  },
  forbidAdd: {
    type: Boolean,
    default: false,
  },
  noLoad: {
    type: Boolean,
    default: false,
  },

});

const input = ref();

const options = computed(() =>
  props.ressource.map((o) => {
    return { value: o.id, label: o.name };
  })
);

function addOption(query) {
    props.create({ name: query })
    .then((data) => {
      emit("update:modelValue", [].concat(props.modelValue).concat([data.id]));
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

function removeOption(option) {
  emit(
    "update:modelValue",
    props.modelValue.filter((v) => v != option)
  );
}

function change(v) {
  emit("update:modelValue", v.filter(e=>typeof e === 'number'));
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
