<!-- Component inspired from https://alligator.io/vuejs/vue-pagination-component/ -->
<template>
  <nav v-if="!(isInFirstPage && isInLastPage) && totalPages != 0">
    <ul class="pagination">
      <li class="page-item" :class="{ disabled: isInFirstPage }">
        <button
          class="page-link"
          @click="onClickFirstPage"
          aria-label="Go to first page"
        >
          First
        </button>
      </li>

      <li class="page-item" :class="{ disabled: isInFirstPage }">
        <button
          class="page-link"
          @click="onClickPreviousPage"
          aria-label="Go to previous page"
        >
          Previous
        </button>
      </li>

      <li
        v-for="page in pages"
        class="page-item"
        :key="page.name"
        :class="{ active: isPageActive(page.name) }"
      >
        <button
          class="page-link"
          @click="onClickPage(page.name)"
          :aria-label="`Go to page number ${page.name}`"
        >
          {{ page.name }}
        </button>
      </li>

      <li class="page-item" :class="{ disabled: isInLastPage }">
        <button
          class="page-link"
          @click="onClickNextPage"
          aria-label="Go to next page"
        >
          Next
        </button>
      </li>

      <li class="page-item" :class="{ disabled: isInLastPage }">
        <button
          class="page-link"
          @click="onClickLastPage"
          aria-label="Go to last page"
        >
          Last
        </button>
      </li>
    </ul>
  </nav>
</template>
<script>
/*
    Paginate items
  */
export default {
  name: "pagination",
  template: "#pagination",
  props: {
    maxVisibleButtons: {
      type: Number,
      required: false,
      default: 3,
    },
    totalPages: {
      type: Number,
      required: true,
    },
    total: {
      type: Number,
      required: true,
    },
    perPage: {
      type: Number,
      required: true,
    },
    currentPage: {
      type: Number,
      required: true,
    },
  },
  computed: {
    startPage() {
      if (this.currentPage === 1) {
        return 1;
      }

      if (this.currentPage === this.totalPages) {
        return Math.max(this.totalPages - this.maxVisibleButtons + 1, 1);
      }

      return this.currentPage - 1;
    },
    endPage() {
      return Math.min(
        this.startPage + this.maxVisibleButtons - 1,
        this.totalPages
      );
    },
    pages() {
      const range = [];
      for (let i = this.startPage; i <= this.endPage; i += 1) {
        range.push({
          name: i,
          isDisabled: i === this.currentPage,
        });
      }

      return range;
    },
    isInFirstPage() {
      return this.currentPage === 1;
    },
    isInLastPage() {
      return this.currentPage === this.totalPages;
    },
  },
  methods: {
    onClickFirstPage() {
      this.$emit("pagechanged", 1);
    },
    onClickPreviousPage() {
      this.$emit("pagechanged", this.currentPage - 1);
    },
    onClickPage(page) {
      this.$emit("pagechanged", page);
    },
    onClickNextPage() {
      this.$emit("pagechanged", this.currentPage + 1);
    },
    onClickLastPage() {
      this.$emit("pagechanged", this.totalPages);
    },
    isPageActive(page) {
      return this.currentPage === page;
    },
  },
};
</script>
