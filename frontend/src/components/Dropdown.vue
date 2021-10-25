<template>
  <div :class="show ? 'dropdown show' : 'dropdown'" @focusout="hide">
    <a
      v-if="!button"
      href=""
      :class="classtoogle + ' dropdown-toggle'"
      :id="'button' + _uid"
      @click="toogle"
      >{{ label }}</a
    >
    <button
      v-if="button"
      :class="classtoogle + ' btn dropdown-toggle'"
      :id="'button' + _uid"
      @click="toogle"
    >
      {{ label }}
    </button>
    <div
      :class="show ? 'dropdown-menu show' : 'dropdown-menu'"
      :id="'tooltip' + _uid"
    >
      <router-link
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        v-slot="{ href, navigate }"
      >
        <a :href="href" class="dropdown-item" @click="goto($event, navigate)">{{
          item.label
        }}</a>
      </router-link>
    </div>
  </div>
</template>

<script>
/*
    Emulate Dropdown bootstrap in Vue
    Takes in enter button mode, router links with props label and to
  */
export default {
  name: "simple-dropdown",
  props: {
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
  },
  data() {
    return {
      show: false,
      id: null,
    };
  },
  computed: {},
  methods: {
    toogle(e) {
      e.preventDefault();
      this.show = !this.show;
    },
    hide(e) {
      if (!this.$el.contains(e.relatedTarget)) {
        this.show = false;
      }
    },
    goto(event, navigate) {
      this.show = false;
      navigate(event);
    },
  },
};
</script>
