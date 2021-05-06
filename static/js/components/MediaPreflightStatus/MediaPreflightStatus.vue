<script>
export default {
  name: 'MediaPreflightStatus',
  props: {
    preflightStatus: {
      type: Object,
      required: true,
      default: () => ({ status: 'pending', warnings: [], errors: [] }),
    },
  },
  computed: {
    status() {
      return this.preflightStatus.status;
    },
    warnings() {
      return this.preflightStatus.warnings;
    },
    errors() {
      return this.preflightStatus.errors;
    },
    checkPassed() {
      if (this.status !== 'completed') {
        return false;
      }
      if (this.warnings.length) {
        return false;
      }
      if (this.errors.length) {
        return false;
      }
      return true;
    },
    tooltipText() {
      if (this.status === 'pending') {
        return 'Preflight check pending';
      }
      if (this.status === 'running') {
        return 'Preflight check running';
      }
      if (this.errors.length) {
        return this.errors.join('<br>');
      }
      if (this.warnings.length) {
        return this.warnings.join('<br>');
      }
      return '';
    },
  },
};
</script>
<template>
  <div
    class="preflight-status"
    :class="{
      'is-pending': status === 'pending',
      'has-warnings': warnings.length,
      'has-errors': errors.length,
    }"
  >
    <!--
    <pre
      class="debug"
      v-text="preflightStatus"
    />
    -->
    <span
      v-if="checkPassed"
      class="label"
    >
      <slot name="default" />
    </span>
    <span
      v-else
      v-tooltip="tooltipText"
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

    &.is-pending {
      cursor: wait;
      opacity: 0.5;
    }

    &.has-warnings {
      color: #ffaa00;
      cursor: pointer;
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
