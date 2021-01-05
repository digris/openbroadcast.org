<script>

import { templateFilters } from 'src/utils/template-filters';
import Visual from '../UI/Visual.vue';

export default {
  name: 'ObjectMergeObject', // sorry for the naming confusion..
  components: {
    visual: Visual,
  },
  filters: templateFilters,
  props: {
    obj: {
      type: Object,
      required: true,
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    numMedia() {
      if (!this.obj.media) {
        return 0;
      }
      return this.obj.media.length;
    },
  },
  methods: {
    select() {
      this.$emit('selectObject', this.obj);
    },
  },
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
      <p>
        {{ obj.name }}
        <span
          v-if="obj.id"
          class="dim"
        >{{ obj.id }}</span>
      </p>
      <p v-if="obj.artistDisplay">
        {{ obj.artistDisplay }}
      </p>
      <p v-if="obj.releaseDisplay">
        {{ obj.releaseDisplay }}
      </p>
      <p v-if="obj.labelDisplay">
        {{ obj.labelDisplay }}
      </p>
      <p v-if="obj.releasedate">
        {{ obj.releasedate }}
      </p>
    </div>
    <div class="meta meta--right">
      <p v-if="obj.media">
        <span class="label">num. tracks</span>
        <span class="value">{{ obj.media.length }}</span>
      </p>
      <p v-if="obj.duration">
        <span class="label">duration</span>
        <span class="value">{{ obj.duration | sToTime }}</span>
      </p>
      <p v-if="obj.created">
        <span class="label">created</span>
        <span class="value">{{ obj.created | date }}</span>
      </p>
      <p v-if="obj.updated">
        <span class="label">updated</span>
        <span class="value">{{ obj.updated | date }}</span>
      </p>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .object-merge-object {

    display: grid;
    grid-gap: .5rem;
    grid-template-columns: 64px auto 160px;

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

    .meta {
      display: flex;
      flex-direction: column;

      &--right {
        > p {
          display: grid;
          grid-gap: .5rem;
          grid-template-columns: auto 80px;

          .label {
            opacity: 0.5;
          }

          .value {
            text-align: right;
          }

        }
      }
    }

  }
</style>
