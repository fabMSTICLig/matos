<template>
  <div
    ref="root"
    :class="show ? 'dropdown show' : 'dropdown'"
    @focusout="hide"
  >
    <a
      v-if="!button"
      :id="'button' + uid"
      href=""
      :class="classtoogle + ' dropdown-toggle'"
      @click.prevent="toogle"
    >{{ label }}</a>
    <button
      v-if="button"
      :id="'button' + uid"
      :class="classtoogle + ' btn dropdown-toggle'"
      @click.prevent="toogle"
    >
      {{ label }}
    </button>
    <div
      :id="'tooltip' + uid"
      :class="show ? 'dropdown-menu show' : 'dropdown-menu'"
    >
      <router-link
        v-for="item in items"
        :key="item.label"
        v-slot="{ href, navigate }"
        :to="item.to"
      >
        <a
          :href="href"
          class="dropdown-item"
          @click="goto($event, navigate)"
        >{{
          item.label
        }}</a>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";
import { v4 as uuidv4 } from "uuid";

defineProps({
  items: {
    type: Array,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  button: {
    type: Boolean,
    required: false,
    default: false,
  },
  classtoogle: {
    type: String,
    required: false,
    default: "",
  },
});
const uid = uuidv4();
const show = ref(false);

const toogle = function () {
  show.value = !show.value;
};
const root = ref(null);
function hide(e) {
  if (root.value && !root.value.contains(e.relatedTarget)) {
    show.value = false;
  }
}
const goto = function (event, navigate) {
  show.value = false;
  navigate(event);
};
</script>
