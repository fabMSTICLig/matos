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
  <ul class="list-group list-group-horizontal d-flew flex-wrap">
    <li
      v-for="item in items"
      :key="item"
      class="list-group-item border rounded"
    >
      {{ item[fieldName] }}
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
  fieldName: {
    type: String,
    required: false,
    default: "name",
  },
});
</script>
