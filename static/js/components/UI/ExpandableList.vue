<script>
export default {
  props: {
    limit: {
      type: Number,
      required: false,
      default: 5,
    },
    separator: {
      type: String,
      required: false,
      default: ',',
    },
  },
  data() {
    return {
      numChildren: 0,
      isExpanded: false,
    };
  },
  computed: {
    isExpandable() {
      return (this.numChildren > this.limit);
    },
    cssVars() {
      return {
        '--separator': `${this.separator}`,
      };
    },
  },
  mounted() {
    this.numChildren = this.$el.childElementCount;
    Array.from(this.$el.children).forEach((el, index) => {
      el.classList.add('list-item');
      if (index >= this.limit) {
        el.classList.add('is-initially-hidden');
      }
    });
  },
  methods: {
    expand() {
      this.isExpanded = true;
    },
    shrink() {
      this.isExpanded = false;
    },
  },
};
</script>
<template>
  <div
    class="expandable-list"
    :class="{'is-expanded': isExpanded}"
    :style="cssVars"
  >
    <slot />
    <div
      v-if="isExpandable"
      class="expandable-list__toggle"
    >
      <span
        v-if="(!isExpanded)"
        @click="expand"
      >
        more
      </span>
      <span
        v-else
        @click="shrink"
      >
        less
      </span>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.expandable-list {
  .list-item {
    &:after {
      //content: var(--separator);
      content: '';
    }
    &:last-of-type {
      &:after {
        content: '';
      }
    }
  }
  .is-initially-hidden {
    display: none;
  }
  &.is-expanded {
    .is-initially-hidden {
      display: unset;
    }
  }
  &__toggle {
    display: inline;

    color: var(--primary-color);

    cursor: pointer;
  }
}
</style>
