<script>
export default {
  name: 'MediaPreflightStatus',
  props: {
    preflightStatus: {
      type: Object,
      required: true,
    },
  },
  computed: {
    checkPassed() {
      return (this.preflightStatus.passed) ? this.preflightStatus.passed : false;
    },
    errors() {
      return this.preflightStatus.errors;
    },
  },
};
</script>
<template>
  <div
    class="preflight-status"
    :class="{'check-failed': ! checkPassed}"
  >
    <span
      v-if="checkPassed"
      class="label"
    >
      <slot name="default" />
    </span>
    <span
      v-else
      class="label"
    >
      <slot name="default" />
    </span>
  </div>
</template>
<style lang="scss" scoped>
  .preflight-status {
    position: relative;

    display: inline-flex;

    color: #a5a5a5;

    &.check-failed {
      color: orangered;

      cursor: pointer;
    }

    .label {
      position: relative;

      text-transform: uppercase;
    }

  }
</style>
