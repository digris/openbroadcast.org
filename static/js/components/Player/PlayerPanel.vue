<script>

import Visual from '../UI/Visual.vue';

export default {
  name: 'PlayerPanel',
  components: {
    visual: Visual,
  },
  computed: {
    currentMedia() {
      return this.$store.getters['player/currentMedia'];
    },
  },
};
</script>
<style lang="scss" scoped>
  .panel {
    display: grid;
    grid-template-columns: auto 100px;

    &__visual {
      height: 100px;

      background: $white;
      img {
        border: 2px solid red;
      }
    }

  }
</style>
<template>
  <div class="panel">
    <div class="panel__info">
      <div v-if="currentMedia">
        {{ currentMedia.name }}
      </div>
    </div>
    <div class="panel__visual">
      <visual
        v-if="currentMedia"
        :url="currentMedia.image"
      />
    </div>
  </div>
</template>
