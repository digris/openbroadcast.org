<script>

export default {
  name: 'PlayerListItem',
  props: {
    item: {
      type: Object,
      required: true,
    },
  },

};
</script>
<template>
  <div class="item">
    <div class="item__panel">
      {{ item.name }}
    </div>
    <div class="item__media">
      <slot />
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .item {

    // background: $primary-color;

    &__panel {
      padding: 0.5rem;
      border-bottom: 1px solid $light-grey;
    }
    &__media {
      border-bottom: 1px solid $light-grey;
    }
  }
</style>
