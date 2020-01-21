<script>
import Waveform from './waveform.vue';

export default {
  components: {
    Waveform,
  },
  filters: {
    sec_to_time(value) {
      return ms_to_time(value * 1000);
    },
    ms_to_time(value) {
      return ms_to_time(value);
    },
  },
  props: {
    itemToPlay: {
      type: Object,
      required: true,
    },
  },
  methods: {
    seek(item, e) {
      const x = e.clientX;
      const w = window.innerWidth;
      const p = Math.round((x / w) * 100);
      this.$emit('seek', item, p);
    },
  },
};

const ms_to_time = function (time) {
  if (time === undefined) {
    return '';
  }

  if (time === 0) {
    return '00:00';
  }

  time = Math.abs(time);

  const millis = time % 1000;
  time = parseInt(time / 1000);
  const seconds = time % 60;
  time = parseInt(time / 60);
  const minutes = time % 60;
  time = parseInt(time / 60);
  const hours = time % 24;
  let out = '';

  if (hours && hours > 0) {
    if (hours < 10) {
      out += '0';
    }
    out += `${hours}:`;
  } else {
    // out += '0' + ':';
  }

  if (minutes && minutes > 0) {
    if (minutes < 10) {
      out += '0';
    }
    out += `${minutes}:`;
  } else {
    out += '00' + ':';
  }

  if (seconds && seconds > 0) {
    if (seconds < 10) {
      out += '0';
    }
    out += `${seconds}`;
  } else {
    out += '00' + '';
  }

  return out.trim();
};


</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .item-to-play {
      //background: $primary-color-a;
      .item-to-play-header {
        color: blue;
      }

      .item-to-play-content {
        .item {
          color: #5a5a5a;
          background: #fafafa;
          border-bottom: 1px solid #eaeaea;
          margin-bottom: 4px;

          &.is-playing {
            background: $primary-color-a-bg-light;
          }

          .primary-content {
            padding: 2px 4px;
            display: flex;

            .meta {
              padding-left: 10px;
              flex-grow: 1;
            }

            .time {
              padding-right: 10px;

              small {
                opacity: 0.5;
              }
            }
          }
        }
      }
    }
</style>

<template>
  <div class="item-to-play">
    <div class="item-to-play-header">
      <span v-if="item_to_play">*{{ item_to_play.name }} - {{ item_to_play.ct }}*</span>
    </div>

    <div class="item-to-play-content">
      <div
        v-for="item in item_to_play.items"
        :key="item.key"
        class="item"
        :class="{ 'is-playing': item.is_playing }"
      >
        <div class="primary-content">
          <div class="controls">
            <span
              v-if="(! item.is_playing)"
              @click="$emit('play', item)"
            >
              (( play ))
            </span>
            <span
              v-else
              @click="$emit('pause', item)"
            >
              (( pause ))
            </span>
          </div>

          <div class="meta">
            <!--<span>Playing: {{ item.is_playing }}{{ item.playhead_position }}</span><br>-->
            <span>{{ item.content.name }}</span>
            <br>
            <span>{{ item.content.artist_display }}</span>
            |
            <span>{{ item.content.release_display }}</span>
          </div>

          <div class="time">
            <small v-if="item.is_playing">{{ item.playhead_position_ms | ms_to_time }}</small>
            {{ item.duration | ms_to_time }}
            <br>
            <!--
                        {{ item.from | ms_to_time }} - {{ item.to | ms_to_time }}
                        -->
            <!--<br>
                        {{ item.fade_to }} - {{ item.fade_from }}-->
            <br>
          </div>

          <div class="actions">
            (( actions ))
          </div>
        </div>

        <div v-if="item.errors">
          <div
            v-for="(error, index) in item.errors"
            :key="(`error-${index}`)"
          >
            {{ error }}
          </div>
        </div>

        <div
          v-if="item.is_playing"
          class="playhead"
          @click="seek(item, $event)"
        >
          <waveform
            :key="item.uuid"
            :item="item"
          />
        </div>
      </div>
    </div>
  </div>
</template>
