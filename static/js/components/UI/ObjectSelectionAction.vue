<script>
import { EventBus } from 'src/eventBus';

export default {
  name: 'ObjectSelectionAction',
  props: {
    minSelected: {
      type: Number,
      required: false,
      default: 1,
    },
    maxSelected: {
      type: Number,
      required: false,
      default: undefined,
    },
    dispatchEvent: {
      type: String,
      required: false,
      default: undefined,
    },
  },
  computed: {
    selection() {
      return this.$store.getters['objectSelection/selection'];
    },
    numSelected() {
      return this.$store.getters['objectSelection/numSelected'];
    },
    isDisabled() {
      if (this.minSelected && this.numSelected < this.minSelected) {
        return true;
      }
      if (this.maxSelected && this.numSelected > this.maxSelected) {
        return true;
      }
      return false;
    },
    isEnabled() {
      return !this.isDisabled;
    },
  },
  methods: {
    click() {
      if (this.isDisabled) {
        return;
      }
      if (this.selection && this.dispatchEvent) {
        // TODO: refactor all events to `eventBus`
        const e = new CustomEvent(this.dispatchEvent, { detail: this.selection });
        window.dispatchEvent(e);
        EventBus.$emit(`${this.dispatchEvent}`, { selection: this.selection });
      }
    },
  },
};
</script>
<style lang="scss" scoped>
    .object-selection-action {

      display: flex;

      padding: 3px 0.5rem 3px 0.5rem;

      color: var(--primary-color);

      cursor: pointer;

      &:hover {
        background: var(--primary-color-light);
      }

      &.is-disabled {
        color: var(--text-color-disabled);

        background: transparent;

        cursor: not-allowed;
      }

      .title {
        flex-grow: 1;
      }
    }
</style>
<template>
  <div
    class="object-selection-action"
    :class="{'is-disabled': isDisabled, 'is-enabled': isEnabled}"
    @click="click"
  >
    <div class="title">
      <slot name="default" />
    </div>
    <div
      v-if="isEnabled"
      class="count"
    >
      {{ numSelected }}
    </div>
  </div>
</template>
