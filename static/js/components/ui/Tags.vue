<script>
export default {
  name: 'Tags',
  props: {
    tags: {
      type: Array,
      default: () => [],
    },
    theme: {
      type: String,
      default: 'dark',
      validator(value) {
        return ['dark', 'light'].indexOf(value) !== -1;
      },
    },
  },
};
</script>
<style lang="scss" scoped>
    .tags {
      display: inline-block;

      &__tag {
        display: inline-flex;
        margin: 0 2px 2px 0;
        padding: 2px 4px;

        color: #fff;
        white-space: nowrap;
        text-transform: uppercase;

        background: #333;
      }
    }
</style>
<template>
  <div
    v-if="tags && tags.length"
    class="tags"
  >
    <div
      v-for="(tag, index) in tags"
      :key="`tag-${index}`"
      class="tags__tag"
    >
      {{ tag }}
    </div>
  </div>
</template>
