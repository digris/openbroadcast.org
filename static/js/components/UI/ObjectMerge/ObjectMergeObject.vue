<script>

import Visual from '..//Visual.vue';

const DEBUG = true;

export default {
  name: 'ObjectMergeObject', // sorry for the naming confusion..
  components: {
    visual: Visual,
  },
  props: {
    obj: {
      type: Object,
      required: true,
    },
    isSelected: {
      type: Boolean,
      default: false,
    }
  },
  methods: {
    select() {
      this.$emit('selectObject', this.obj);
    },
  },
  computed: {
    numMedia() {
      if(! this.obj.media) {
        return 0;
      }
      return this.obj.media.length;
    },
  }
};
</script>
<template>
  <div
    class="object-merge-object"
    :class="{'is-selected': isSelected}"
    @click="select"
  >
    <div class="visual">
      <visual :url="obj.image" />
    </div>

    <div class="meta">
      {{ obj.name }}
      <p v-if="obj.releasedate">
        {{ obj.releasedate }}
      </p>
    </div>

    <div class="meta">
      Tracks: {{ numMedia }}
      <br>
      ID: {{ obj.id }}
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .object-merge-object {

    display: grid;
    grid-gap: .5rem;
    grid-template-columns: 64px auto 120px;

    margin-bottom: .5rem;

    border-left: 4px solid transparent;

    cursor: pointer;


    &:hover {
      background: rgba(#fff, 0.08);
    }


    &.is-selected {
      background: rgba(#fff, 0.12);

      border-left: 4px solid var(--primary-color);
    }

    .visual {
      height: 64px;
    }

  }
</style>
