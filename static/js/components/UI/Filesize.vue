<script>
import prettyBytes from 'pretty-bytes';

export default {
  name: 'Filesize',
  props: {
    filesize: {
      type: Number,
      default: null,
    },
  },
  computed: {
    fsDisplay() {
      if (!this.filesize) {
        return '-';
      }
      return prettyBytes(this.filesize);
    },
  },
};
</script>

<template>
  <div
    class="filesize"
  >
    {{ fsDisplay }}
  </div>
</template>
