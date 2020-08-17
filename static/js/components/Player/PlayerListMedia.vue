<script>

import { templateFilters } from 'src/utils/template-filters';

const DEBUG = true;

export default {
  name: 'PlayerListMedia',
  filters: templateFilters,
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  computed: {
    currentMedia() {
      return this.$store.getters['player/currentMedia'];
    },
    isCurrent() {
      return (this.media === this.currentMedia);
    },
    state() {
      if (!this.isCurrent) {
        return 'stopped';
      }
      return 'playing';
    },
  },
  methods: {
    play() {
      if (DEBUG) console.debug('play');
      this.$emit('play', this.media);
      this.playByMediaObj(this.media);
    },
    // mapped vuex actions
    playByMediaObj(media) {
      this.$store.dispatch('player/playByMediaObj', { media });
    },
  },
};
</script>
<template>
  <div
    class="media"
    :class="{'media--is-current': isCurrent}"
  >
    <div class="media__controls">
      <span
        v-if="(state === 'stopped')"
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-play-arrow" />
      </span>
      <span
        v-if="(state === 'playing')"
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-pause" />
      </span>
    </div>
    <div class="media__info">
      <span>{{ media.name }}</span>
      <span>
        <span>{{ media.artistDisplay }}</span>
        |
        <span>{{ media.releaseDisplay }}</span>
      </span>
    </div>
    <div class="media__time">
      0:00 - {{ media.duration|sToTime }}
    </div>
    <div class="media__secondary-controls">
      <span
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-heart-o" />
      </span>
      <span
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-remove-circle-o" />
      </span>
      <span
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-clear" />
      </span>
      <span
        class="action"
        @click.prevent="play"
      >
        <i class="icn icn-playlist-add" />
      </span>
    </div>
    <div class="media__progress" />
  </div>
</template>
<style lang="scss" scoped>

  @mixin action($size: 32px, $hover-bg-color: $primary-color) {

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: $size;
    height: $size;

    font-size: $size;

    border-radius: 50%;
    cursor: pointer;
    &:hover {
      color: $white;

      background: $hover-bg-color;
      transform: scale(1.1);

      .icn {
        font-size: 80%;
      }

    }
  }

  @mixin secondary-action($size: 24px, $hover-color: $primary-color) {

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: $size;
    height: $size;

    font-size: $size;

    cursor: pointer;

    &:hover {
      color: $hover-color;

      transform: scale(1.1);
    }
  }

  .media {
    display: grid;
    grid-template-areas: "controls info time secondary-controls" "progress progress progress progress";
    grid-template-rows: 48px 2px;
    grid-template-columns: 60px auto 100px 120px;

    transition: background 200ms;

    &--is-current {
      background: $secondary-color-light;
    }

    &__controls,
    &__info,
    &__time,
    &__secondary-controls {
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    &__controls {
      grid-area: controls;
      padding-left: 10px;
      .action {
        @include action($hover-bg-color: $secondary-color);
      }
    }
    &__info {
      grid-area: info;
    }
    &__time {
      grid-area: time;
    }
    &__secondary-controls{
      flex-direction: row;
      grid-area: secondary-controls;
      align-items: center;
      .action {
        @include secondary-action($size: 20px);
        margin: 0 0 0 4px;
      }
    }
    &__progress{
      grid-area: progress;

      // background: rgba($secondary-color, 0.2);
      background: #eee;
    }
  }
</style>
