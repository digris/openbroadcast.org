<script>
export default {
  name: 'ObjectSingleAction',
  props: {
    objCt: {
      type: String,
      required: true,
    },
    objUuid: {
      type: String,
      required: true,
    },
    dispatchEvent: {
      type: String,
      required: true,
    },
  },
  computed: {
    key() {
      return `${this.objCt}:${this.objUuid}`;
    },
  },
  methods: {
    click() {
      // TODO: refactor all events to `eventBus`
      const e = new CustomEvent(this.dispatchEvent, {detail: [this.key]});
      window.dispatchEvent(e);
      // EventBus.$emit(`${this.dispatchEvent}`, {selection: this.selection});
    },
  },
};
</script>
<template>
  <div
    class="object-single-action"
    @click="click"
  >
    <div class="title">
      <slot name="default" />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.object-single-action {
  display: flex;

  padding: 3px 0.5rem 3px 0.5rem;

  color: var(--primary-color);

  cursor: pointer;

  &:hover {
    background: var(--primary-color-light);
  }

  .title {
    flex-grow: 1;
  }
}
</style>
