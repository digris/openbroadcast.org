<script>
import dayjs from 'dayjs';

export default {
  name: 'Date',
  props: {
    value: {
      type: String,
      required: true,
    },
    includeTime: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    localeOptions() {
      const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      };
      // if (this.includeTime) {
      //   options.hour = '2-digit';
      //   options.minute = '2-digit';
      // }
      return options;
    },
    valueDisplay() {
      const ts = dayjs(this.value).$d;
      return ts.toLocaleString(this.locale, this.localeOptions);
      // return ts;
    },
  },
};
</script>

<template>
  <span
    class="date"
  >
    {{ valueDisplay }}
  </span>
</template>

<style lang="scss" scoped>
  .date {
    display: inline-flex;
  }
</style>
