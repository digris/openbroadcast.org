<script>
export default {
  name: 'TagList',
  props: {
    tags: {
      type: Array,
      required: true,
    },
  },
  computed: {
    genreTags() {
      return this.tags.filter((t) => t.type === 'genre');
    },
    moodTags() {
      return this.tags.filter((t) => t.type === 'mood');
    },
    sortedTags() {
      const primary = [...this.genreTags, ...this.moodTags];
      const secondary = this.tags.filter((t) => !primary.includes(t));
      return [...primary, ...secondary];
    },
  },
  // mounted() {
  //   const observer = new IntersectionObserver((entries) => {
  //     entries.forEach((entry) => {
  //       console.debug(entry.isIntersecting);
  //     });
  //   });
  //   observer.observe(this.$el);
  // },
};
</script>
<template>
  <div
    class="tag-list"
  >
    <span
      v-for="(tag, index) in sortedTags"
      :key="`tags-tag-${index}`"
      v-tooltip="tag.type"
      class="tag"
      :class="`tag--${tag.type}`"
    >{{ tag.name }}</span>
  </div>
</template>
<style lang="scss" scoped>

$c-genre: red;
$c-mood: #00bb73;
$c-descriptive: #008cd7;

.tag-list {
  .tag {
    display: inline-flex;
    margin: 0 3px 3px 0;
    padding: 2px 6px 1px;
    color: #555;
    font-size: 90%;
    text-transform: uppercase;
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-left: 2px solid #a5a5a5;

    &--genre {
      border-left-color: $c-genre;
    }

    &--mood {
      border-left-color: $c-mood;
    }

    &--descriptive {
      border-left-color: $c-descriptive;
    }
  }
}
</style>
