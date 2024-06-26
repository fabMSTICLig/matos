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
  <div v-if="show">
    <div class="modal-backdrop show" />
    <div
      class="modal"
      :class="{ show: show }"
      :style="{ display: show ? 'block' : 'none' }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div v-if="!hideHeader" class="modal-header">
            <h5 class="modal-title">
              {{ title }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
              @click.prevent="handleClose()"
            ></button>
          </div>
          <div class="modal-body">
            <slot>
              <p>{{ content }}</p>
            </slot>
          </div>
          <div v-if="!hideFooter" class="modal-footer">
            <button
              v-if="!confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="handleClose()"
            >
              Ok
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="handleConfirm()"
            >
              Oui
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-danger"
              @click.prevent="handleReject()"
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
  props: {
    content: {
      type: null,
      default: "",
    },
    hideHeader: {
      type: Boolean,
      default: false,
    },
    hideFooter: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "Title",
    },
    show: {
      type: Boolean,
      default: false,
    },
    confirmFooter: {
      type: Boolean,
      default: false,
    },
    resolve: {
      type: Function,
    },
  },
  setup(props) {
    function handleClose() {
      if (props.resolve) {
        props.resolve(null);
      }
    }

    function handleConfirm() {
      if (props.resolve) {
        props.resolve(true);
      }
    }

    function handleReject() {
      if (props.resolve) {
        props.resolve(false);
      }
    }

    return {
      handleClose,
      handleConfirm,
      handleReject,
    };
  },
};
export default Modal;
</script>
