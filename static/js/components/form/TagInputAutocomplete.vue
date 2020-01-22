<script>
export default {
  name: 'TagInputAutocomplete',

  props: {
    items: {
      type: Array,
      required: false,
      default: () => [],
    },
    isAsync: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      isOpen: false,
      results: [],
      search: '',
      isLoading: false,
      arrowCounter: 0,
    };
  },
  watch: {
    items(val, oldValue) {
      // actually compare them
      if (val !== oldValue) {
        this.results = val;
        this.isLoading = false;
        this.isOpen = true;
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  destroyed() {
    document.removeEventListener('click', this.handleClickOutside);
  },

  methods: {
    onChange() {
      // Let's warn the parent that a change was made
      this.$emit('input', this.search);

      // Is the data given by an outside ajax request?
      if (this.isAsync) {
        if (this.items.length < 1) {
          this.isLoading = true;
        }
      } else {
        // Let's  our flat array
        this.filterResults();
        this.isOpen = true;
      }
    },

    filterResults() {
      // first uncapitalize all the things
      this.results = this.items.filter((item) => item.toLowerCase().indexOf(this.search.toLowerCase()) > -1);
    },

    setResult(result) {
      this.arrowCounter = -1;
      this.isOpen = false;
      this.$emit('result', result);
      this.search = '';
    },
    onArrowDown(evt) {
      if (this.arrowCounter < this.results.length) {
        this.arrowCounter = this.arrowCounter + 1;
      }
    },
    onArrowUp() {
      if (this.arrowCounter > 0) {
        this.arrowCounter = this.arrowCounter - 1;
      }
    },
    onEnter() {
      // no result from autocomplete
      if (this.arrowCounter < 0) {
        this.setResult(this.search);
      } else {
        this.setResult(this.results[this.arrowCounter]);
      }
    },
    handleClickOutside(evt) {
      if (!this.$el.contains(evt.target)) {
        this.isOpen = false;
        this.arrowCounter = -1;
      }
    },
  },
};
</script>

<template>
  <div class="autocomplete">
    <input
      v-model="search"
      type="text"
      maxlength="50"
      placeholder="Add Tag"
      @input="onChange"
      @keydown.down.prevent="onArrowDown"
      @keydown.up.prevent="onArrowUp"
      @keydown.enter.prevent="onEnter"
      @keydown.188.prevent="onEnter"
    >
    <ul
      v-show="isOpen"
      class="autocomplete__results"
    >
      <li
        v-if="isLoading"
        class="loading"
      >
        Loading tags...
      </li>
      <li
        v-for="(result, i) in results"
        v-else
        :key="i"
        class="autocomplete__result"
        :class="{ 'is-active': i === arrowCounter }"
        @click="setResult(result)"
      >
        {{ result }}
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
    .autocomplete {
      position: relative;

      display: inline-block;
      width: 100%;

      input {
        width: 100%;
        height: 22px;
        padding: 0 0.5rem;

        line-height: 22px;
      }

      &__results {
        position: absolute;
        z-index: 10;

        min-width: 100%;
        min-height: 40px;
        margin: 0;
        padding: 0;
        // border: 1px solid #eeeeee;
        overflow: auto;

        background: white;
        border: 1px solid #ededed;
        // border-top: 0;
        box-shadow: 1px 2px 3px 1px rgba(#000, 0.2);
      }

      &__result {
        padding: 0.5rem;

        text-align: left;

        list-style: none;
        cursor: pointer;

        &.is-active,
        &:hover {
          background: #e2d7f9;
        }
      }
    }

</style>
