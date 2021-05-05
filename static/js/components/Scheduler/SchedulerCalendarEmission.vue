<script>

import { templateFilters } from 'src/utils/template-filters';
import { hexToRGBA } from './utils';

const DEBUG = false;

export default {
  name: 'SchedulerCalendarEmission',
  filters: templateFilters,
  props: {
    emission: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isHover: false,
    };
  },
  computed: {
    style() {
      const color = this.emission.obj.color;
      return {
        backgroundColor: (this.isHover) ? hexToRGBA(color, 1) : hexToRGBA(color, 0.50),
        borderColor: hexToRGBA(color, 1),
      };
    },
  },
  methods: {
    dblclick() {
      this.$emit('dblclick', this.emission.obj.uuid);
      this.isHover = false;
    },
    onMouseOver() {
      this.$emit('mouseover', this.emission.obj.co.uuid);
      this.isHover = true;
    },
    onMouseLeave() {
      this.$emit('mouseleave');
      this.isHover = false;
    },

  },
};
</script>
<style lang="scss" scoped>

        // background: red;
        .emission {
          position: relative;
          display: flex;
          flex-direction: column;
          height: calc(100% - 1px);
          // border: 1px solid rgba(0, 0, 0, 0.25);
          margin: 1px 0 1px 1px;
          background: rgba(255, 255, 255, 0.8);
          border-top: 2px solid #fff;
          border-bottom: 2px solid #fff;
          cursor: pointer;
          transition: background 100ms;

          &:hover {
            z-index: 90;
            // background: rgba(126, 235, 157, 0.85);
            min-height: 20px;
          }

          &__title {
            // background: rgba(0, 0, 0, .025);
            padding: 0 4px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
          }

          &:hover & {
            &__title {
              z-index: 91;
              overflow: visible;
              white-space: normal;
            }
          }

          &.is-highlighted {
            background: rgba(255, 0, 21, 0.85) !important;
            border-color: rgba(255, 0, 21, 0.85) !important;
          }

          &.is-dragged {
            opacity: 0.2;
          }

          // detail block, visible on hover
          &__details {
            position: absolute;
            top: -2px;
            left: calc(100% + 4px);
            z-index: 999;
            min-width: 140px;
            padding: 2px 4px 2px;
            color: white;
            text-align: center;
            background: #000;

            &__title {
              margin-top: 4px;
            }

            &__visual {
              max-width: 130px;
              margin-top: 8px;
              text-align: center;

              img {
                max-width: 90px;
                // object-fit: fill;
              }
            }

            &__appendix {
              margin: 4px 0 4px;
            }
          }
        }
</style>

<template>
  <div
    :style="style"
    :class="{ 'is-highlighted': emission.highlighted, 'is-dragged': emission.dragged }"
    class="emission"
    @dblclick="dblclick"
    @mouseover="onMouseOver"
    @mouseleave="onMouseLeave"
  >
    <div
      class="emission__title"
    >
      <span v-if="emission.obj.series">
        {{ emission.obj.series }}
        <!--
                <br>
                <small>{{ emission.obj.name }}</small>
                -->
      </span>
      <span v-else>
        {{ emission.obj.name }}
      </span>
    </div>
    <div
      v-if="isHover"
      class="emission__details"
    >
      <div
        class="emission__details__title"
      >
        <span v-if="emission.obj.series">
          {{ emission.obj.series }}
          <br>
          <span>{{ emission.obj.name }}</span>
        </span>
        <span v-else>
          {{ emission.obj.name }}
        </span>
      </div>
      <div
        v-if="emission.obj.image"
        class="emission__details__visual"
      >
        <img :src="emission.obj.image">
      </div>
      <div
        class="emission__details__appendix"
      >
        <span>
          {{ emission.obj.timeStart|date('HH:mm') }}
          -
          {{ emission.obj.timeEnd|date('HH:mm') }}
        </span>
      </div>
    </div>
  </div>
</template>
