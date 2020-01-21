<script>

// NOTE:
// this is the vue-pendant of django template 'templates/layout_base.html'
// vue-version is used to handle apps with sidebar

const DEBUG = true;

export default {
  name: 'LayoutBase',
  props: {
    fullscreen: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    fullscreen(a, n) {
      if (DEBUG) console.debug('fullscreen', this.fullscreen);
      if (this.fullscreen) {
        this.enterFullscreen();
      } else {
        this.exitFullscreen();
      }
    },
  },
  methods: {
    enterFullscreen() {
      if (DEBUG) console.debug('enterFullscreen');
      document.body.classList.add('is-fullscreen');
    },
    exitFullscreen() {
      if (DEBUG) console.debug('exitFullscreen');
      document.body.classList.remove('is-fullscreen');
    },
  },
};
</script>

<template>
  <div class="content">
    <div class="content__primary">
      <slot />
    </div>
    <div class="content__sidebar">
      <slot name="sidebar" />
    </div>
  </div>
</template>
