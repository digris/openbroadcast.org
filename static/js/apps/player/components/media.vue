<script>
import { templateFilters } from 'src/utils/template-filters';

const DEBUG = false;

export default {
  components: {

  },
  filters: templateFilters,
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      seek_active: false,
      seek_position: null,
      is_hover: false,
    };
  },
  computed: {
    position() {
      return (this.item.playhead_position > 0.3) ? this.item.playhead_position - 0.3 : 0;
    },
  },
  mounted() {
    if (DEBUG) console.debug('media - mounted');
  },
  methods: {
    seek(item, e) {
      const x = e.clientX;
      // const w = e.target.getBoundingClientRect().width;
      const w = window.innerWidth;
      const p = Math.round((x / w) * 100);
      this.$emit('seek', item, p);
    },
    seek_move(e) {
      this.seek_position = Math.round((e.clientX / window.innerWidth) * 100);
    },
    seek_enter() {
      // console.log('seek_enter > add listener', e);
      document.removeEventListener('mousemove', this.seek_move);
      document.addEventListener('mousemove', this.seek_move);
    },
    seek_leave() {
      // console.log('seek_leave > remove listener', e);
      document.removeEventListener('mousemove', this.seek_move);
    },
    remove(item) {
      this.$emit('remove', item);
    },
    collect(item) {
      const e = new CustomEvent('collector:collect', { detail: [item] });
      window.dispatchEvent(e);
    },
  },
};

</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .item {
      position: relative;
      color: #5a5a5a;
      background: #fafafa;
      border-bottom: 1px solid #eaeaea;

      &.is-playing {
        background: $primary-color-a-bg-light;
      }

      &.has-errors {
        background: #fffdea;
        cursor: not-allowed;

        .primary-content {
          opacity: 0.5;
          filter: grayscale(100);
        }
      }

      .primary-content {
        display: flex;
        padding: 2px 4px;

        .controls {
          display: flex;
          align-items: center;
          justify-content: center;

          span {
            display: block;
            width: 20px;
            height: 20px;
            padding-top: 2px;
            text-align: center;
            cursor: pointer;
            opacity: 0.75;
          }
        }

        .meta {
          flex-grow: 1;
          padding-left: 10px;
        }

        .time {
          padding-top: 8px;
          padding-right: 10px;
          font-size: 90%;

          small {
            opacity: 0.5;
          }
        }

        .actions {
          display: flex;
          align-items: center;
          justify-content: center;

          span {
            display: block;
            width: 20px;
            height: 20px;
            padding-top: 2px;
            text-align: center;
            cursor: pointer;
            opacity: 0.75;
          }
        }

        .__expandable-actions {
          position: absolute;
          top: 0;
          right: 0;
          z-index: 20;
          width: 20px;
          height: 100%;
          background: red;
        }
      }

      .errors {
        padding: 0 0 2px 34px;
        color: #d47327;
        font-size: 90%;
      }

      .playhead {
        position: relative;
        height: 10px;
        cursor: crosshair;

        .progress-container {
          position: absolute;
          top: 5px;
          z-index: 9;
          width: 100%;
          height: 2px;
          background: white;

          .progress-indicator {
            position: absolute;
            top: 0;
            left: 0;
            width: 25%;
            height: 2px;
            background: $primary-color-a;
          }
        }

        .seek-container {
          position: absolute;
          top: 0;
          z-index: 10;
          display: none;
          width: 50%;
          height: 12px;
          background: rgba(255, 165, 0, 0.05);
          border-right: 1px solid $primary-color-b;
        }

        &:hover {
          .seek-container {
            display: block;
          }
        }
      }
    }
</style>

<template>
  <div
    :key="item.key"
    class="item"
    :class="{ 'is-playing': item.is_playing, 'has-errors': item.errors.length }"
    @mouseover="is_hover=true"
    @mouseleave="is_hover=false"
  >
    <div class="primary-content">
      <div class="controls">
        <span
          v-if="(! item.is_playing)"
          @click="$emit('play', item)"
        >
          <i class="fa fa-play" />
        </span>
        <span
          v-else
          @click="$emit('pause', item)"
        >
          <i class="fa fa-pause" />
        </span>
      </div>
      <div class="meta">
        <span>{{ item.content.name }}</span>
        <br>
        <a
          href="#"
          @click.prevent="$emit('visit', item.content, 'artist')"
        >{{ item.content.artist_display }}</a>
        |
        <a
          href="#"
          @click.prevent="$emit('visit', item.content, 'release')"
        >{{ item.content.release_display }}</a>
      </div>
      <div class="time">
        <small v-if="item.is_buffering">buff</small>
        <small v-if="(! item.is_buffering && item.is_playing)">
          {{ item.playhead_position_ms | msToTime }}
        </small>
        {{ item.duration | msToTime }}
      </div>
      <div class="actions">
        <span @click="remove(item, $event)">
          <i class="fa fa-ban" />
        </span>
        <span @click="collect(item, $event)">
          <i class="fa fa-plus" />
        </span>
      </div>
    </div>
    <div
      v-if="item.errors.length"
      class="errors"
    >
      <div
        v-for="(error, index) in item.errors"
        :key="('error' + index)"
      >
        <span>Error: {{ error.code }}</span>
        &mdash;
        <span>{{ error.info }}</span>
      </div>
    </div>
    <div
      v-if="item.is_playing"
      class="playhead"
      @click="seek(item, $event)"
      @mouseover="seek_enter(item, $event)"
      @mouseleave="seek_leave(item, $event)"
    >
      <div class="progress-container">
        <div
          class="progress-indicator"
          :style="{ width: position + '%' }"
        />
      </div>
      <div
        class="seek-container"
        :style="{ width: seek_position + '%' }"
      />
    </div>
  </div>
</template>
