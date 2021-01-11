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
    errorDisplay() {
      if (this.errors.length) {
        return this.errors.join(', ');
      }
      return 'Check still running';
    },
  },
};
</script>
<template>
  <div
    class="preflight-status"
    :class="{'check-failed': ! checkPassed, 'has-errors': errors.length}"
  >
    <span
      v-if="checkPassed"
      class="label"
    >
      <slot name="default" />
    </span>
    <span
      v-else
      v-tooltip="errorDisplay"
      class="label"
    >
      <slot name="default" />
    </span>
  </div>
</template>
<style lang="scss" scoped>
  .preflight-status {
    display: inline-flex;
    color: #a5a5a5;

    &.check-failed {
      color: #fcc761;
    }

    &.has-errors {
      color: orangered;
      cursor: pointer;
    }

    .label {
      text-transform: uppercase;
    }

  }
</style>
