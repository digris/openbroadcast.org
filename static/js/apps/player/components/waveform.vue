<script>
export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      greeting: 'Hello',
    };
  },
  computed: {
    position() {
      return (this.item.playhead_position > 0.3) ? this.item.playhead_position - 0.3 : 0;
      // return this.item.playhead_position - 0.3;
    },
    cue_fade_points() {
      const { item } = this;

      const x1 = Math.floor((item.from / item.duration) * 100);
      const x2 = Math.floor((item.fade_to / item.duration) * 100);
      const x3 = Math.floor((item.fade_from / item.duration) * 100);
      const x4 = Math.floor((item.to / item.duration) * 100);

      // console.debug('cue_fade_points', `${x1},30 ${x2},0 ${x3},0 ${x4},30`)

      return ` ${x1},30 ${x1},15 ${x2},0 ${x3},0 ${x4},15 ${x4},30`;
    },
    has_cue_or_fade() {
      const { item } = this;
      // eslint-disable-next-line max-len
      return (item.from > 0 || item.to !== item.duration) || (item.from !== item.fade_to || item.to !== item.fade_from);
    },
    rubberband_points() {
      const { item } = this;

      const x1 = Math.floor((item.from / item.duration) * 100);
      const x2 = Math.floor((item.fade_to / item.duration) * 100);
      const x3 = Math.floor((item.fade_from / item.duration) * 100);
      const x4 = Math.floor((item.to / item.duration) * 100);

      return `0,28 ${x1},28 ${x2},2 ${x3},2 ${x4},28 100,28`;
    },
    mask_left() {
      const { item } = this;
      const x = Math.floor((item.from / item.duration) * 100);
      return `0,0 ${x},0 ${x},30 0,30`;
    },
    mask_right() {
      const { item } = this;
      const x = Math.floor((item.to / item.duration) * 100);
      return `${x},0 100,0 100,30 ${x},30`;
    },
    mask_style() {
      return 'fill:rgba(255,255,255,0.7);';
    },
  },
  methods: {
    seek(e) {
      const x = e.clientX;
      // const w = e.target.getBoundingClientRect().width;
      const w = window.innerWidth;
      const p = Math.round((x / w) * 1000) / 10;
      this.$emit('seek', this.item, p);
    },
  },

};

</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .waveform {
      position: relative;
      height: 30px;
      cursor: crosshair;
      //background: black;
      .waveform-rubberband {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 3;
        width: 100%;
        height: 30px;
      }

      .waveform-image {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 2;
        width: 100%;
        height: 30px;

        img {
          width: 100%;
          height: 30px;
        }
      }

      .progress-container {
        position: absolute;
        top: 0;
        z-index: 99;
        width: 100%;
        height: 100%;

        .progress-indicator {
          position: absolute;
          top: 0;
          left: 0;
          width: 0;
          height: 100%;
          border-right: 1px solid $primary-color-a;
        }
      }
    }

    svg polyline {
      shape-rendering: geometricPrecision;
    }

</style>

<template>
  <div
    class="waveform"
    @click="seek($event)"
  >
    <div class="waveform-rubberband">
      <svg
        width="100%"
        height="30px"
        viewBox="0 0 100 30"
        preserveAspectRatio="none"
      >

        <!-- full size waveform bg -->
        <rect
          width="100%"
          height="30"
          style="fill: rgb(165, 165, 165);"
        />

        <!-- progress bg -->
        <rect
          :width="position"
          height="30"
          style="fill: rgb(34, 34, 34);"
        />

        <!-- cue masks (left & right) -->
        <polygon
          :points="mask_left"
          :style="mask_style"
        />
        <polygon
          :points="mask_right"
          :style="mask_style"
        />

        <!-- waveform image -->
        <image
          v-if="(item.content && item.content.assets.waveform)"
          width="100%"
          height="100%"
          preserveAspectRatio="none"
          :xlink:href="item.content.assets.waveform"
        />

        <polyline
          v-if="has_cue_or_fade"
          :points="rubberband_points"
          style=" fill: none;stroke: rgb(102, 51, 204);"
          stroke-width="0.3"
        />

      </svg>
    </div>
    <div class="progress-container">
      <div
        class="progress-indicator"
        :style="{ width: position + '%' }"
      />
    </div>
  </div>
</template>
