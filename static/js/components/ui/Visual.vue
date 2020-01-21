<script>

import settings from '../../settings';

export default {
  name: 'Visual',
  props: {
    url: {
      type: String,
      required: false,
      default: null,
    },
    zoomUrl: {
      type: String,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      placeholder_image: settings.PLACEHOLDER_IMAGE,
    };
  },
  computed: {
    imageUrl() {
      // TODO: debug hack only
      if (this.url && this.url.endsWith(':8000')) {
        return null;
      }

      return this.url;
    },
  },
};
</script>
<style lang="scss" scoped>
    figure {
      margin: 0;

      img {
        width: 100%;
        height: 100%;

        &.placeholder {
          image-rendering: pixelated;
          opacity: 0.5;
        }
      }
    }
</style>
<template>
  <figure>
    <img
      v-if="(imageUrl)"
      :src="imageUrl"
    >
    <img
      v-else
      :src="placeholder_image"
      class="placeholder"
    >
    <slot name="actions" />
  </figure>
</template>
