<template>
  <div v-if="show">
    <div class="modal-backdrop show"></div>
    <div
      class="modal"
      :class="{ show: show }"
      :style="{ display: show ? 'block' : 'none' }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div v-if="!hideHeader" class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <slot
              ><p>{{ content }}</p></slot
            >
          </div>
          <div class="modal-footer" v-if="!hideFooter">
            <button
              type="button"
              class="btn btn-primary"
              v-if="!confirmFooter"
              @click="close"
            >
              Ok
            </button>
            <button
              type="button"
              class="btn btn-primary"
              v-if="confirmFooter"
              @click="confirm(true)"
            >
              Oui
            </button>
            <button
              type="button"
              class="btn btn-danger"
              v-if="confirmFooter"
              @click="confirm(false)"
            >
              Non
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export const Modal = {
  name: "modal",
  model: {
    prop: "show",
    event: "change"
  },
  props: {
    content: {
      type: null,
      default: ""
    },
    hideHeader: {
      type: Boolean,
      default: false
    },
    hideFooter: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: "Title"
    },
    show: {
      type: Boolean,
      default: false
    },
    confirmFooter: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {};
  },
  computed: {},
  methods: {
    close(e) {
      e.preventDefault();
      this.$emit("change", false);
    },
    confirm(val) {
      this.$emit("confirm", val);
    }
  }
};
export default Modal;

import Vue from "vue";

export function showMsgOk(content) {
  var ComponentClass = Vue.extend(Modal);
  var instance = new ComponentClass({
    propsData: { content: content, show: true, hideHeader: true }
  });
  const div = document.createElement("div");
  document.body.appendChild(div);
  instance.$mount(div);
  instance.$on(["change"], () => {
    document.body.removeChild(instance.$el);
    instance.$destroy(true);
  });
}
export function showMsgConfirm(content) {
  var ComponentClass = Vue.extend(Modal);
  var instance = new ComponentClass({
    propsData: {
      content: content,
      show: true,
      hideHeader: true,
      confirmFooter: true
    }
  });
  const div = document.createElement("div");
  document.body.appendChild(div);
  instance.$mount(div);
  return new Promise((resolve, reject) => {
    instance.$on(["change"], () => {
      document.body.removeChild(instance.$el);
      instance.$destroy(true);
      reject();
    });
    instance.$on(["confirm"], val => {
      document.body.removeChild(instance.$el);
      instance.$destroy(true);
      resolve(val);
    });
  });
}
</script>
