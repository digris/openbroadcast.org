<script>

import Visual from '../ui/Visual.vue';
import { templateFilters } from '../../utils/template-filters';

export default {
  name: 'PlaylistEditorSearchResult',
  filters: templateFilters,
  components: {
    'visual': Visual,
  },
  props: {
    media: {
      type: Object,
      required: true,
    },
    isActive: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {

    };
  },
  methods: {

  },
};
</script>
<template>
  <div
    class="search-result"
    :class="{'is-active': isActive}"
    @click="$emit('click', media)"
  >
    <div class="search-result__visual">
      <visual
        :url="media.image"
      />
    </div>
    <div class="search-result__info">
      <div class="info--primary">
        <strong>{{ media.name }}</strong><br>
        {{ media.artistDisplay }}<br>
        {{ media.releaseDisplay }}
      </div>
      <div class="info--secondary">
        <div class="info__row">
          <span class="label">duration</span>
          <span class="value">{{ media.duration|s_to_time }}</span>
        </div>

        <div class="info__row">
          <span class="label">num. emissions</span>
          <span class="value">{{ media.numEmissions }}</span>
        </div>

        <div class="info__row">
          <span class="label">last emission</span>
          <span class="value">
            <span v-if="media.lastEmission">{{ media.lastEmission|date('MMM. D, YYYY') }}</span>
            <span v-else>-</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .search-result {
    display: grid;
    grid-column-gap: 10px;
    grid-template-columns: 64px auto;

    padding: 4px;

    cursor: pointer;

    &:hover,
    &.is-active, {
      /*background: blue;*/
      background: var(--secondary-color-light);
      /*background: v(page-bg-color);*/
    }

    &__visual {
      // background: yellow;
      height: 64px;
    }
    &__info {
      display: grid;
      grid-column-gap: 10px;
      grid-template-columns: auto 220px;

    }

    .info {
      &--secondary {

      }
      &__row {
        display: flex;
        .label {
          flex-grow: 1;

          opacity: .7;
        }
      }
    }


  }
</style>
