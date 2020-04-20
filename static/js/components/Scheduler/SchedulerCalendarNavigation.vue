<script>

import { backgroundColors } from './constants';
import ColorChooser from '../UI/ColorChooser.vue';

const DEBUG = false;

export default {
  name: 'SchedulerCalendarNavigation',
  components: {
    'color-chooser': ColorChooser,
  },
  props: {
    settings: {
      type: Object,
      required: false,
      default() {
        return {};
      },
    },
    isFullscreen: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      emissionColors: backgroundColors,
    };
  },
  computed: {
    numDays() {
      if (this.settings && this.settings.numDays) {
        return this.settings.numDays;
      }
      return null;
    },
    snapMinutes() {
      if (this.settings && this.settings.snapMinutes) {
        return this.settings.snapMinutes;
      }
      return null;
    },
    emissionColor() {
      if (this.settings && this.settings.emissionColor != undefined) {
        return this.settings.emissionColor;
      }
      return null;
    },
  },
  methods: {

  },
};
</script>
<style lang="scss" scoped>
    .calendar-navigation {
      display: flex;

      .action {
        display: inline-flex;
        padding: 1px 8px;

        background: white;
        border: 1px solid #dadada;
        cursor: pointer;

        &:hover {
          color: white;

          background: #63c;
          border-color: #63c;
          border-radius: 2px;
        }

        &.is-current {
          border-color: #63c;
        }
      }

      &__center {
        display: flex;
        flex-grow: 1;
        justify-content: center;

        .action {
          margin-right: 2px;
          margin-left: 2px;
        }
      }

      &__left {
        .action {
          margin-right: 4px;
        }
      }

      &__right {
        .action {
          margin-left: 4px;
        }
      }
    }
</style>

<template>
  <div class="calendar-navigation">
    <div class="calendar-navigation__left">
      <span
        class="action"
        @click.prevent="$emit('updateDaysOffset', 7)"
      >
        &#x3C; Week
      </span>
      <span
        class="action"
        @click.prevent="$emit('updateDaysOffset', 1)"
      >
        &#x3C; Day
      </span>
    </div>

    <div class="calendar-navigation__center">
      <span
        class="action"
        @click.prevent="$emit('decreaseVerticalSize')"
      >
        -
      </span>
      <span
        class="action"
        @click.prevent="$emit('increaseVerticalSize')"
      >
        +
      </span>
      <span
        :class="{ 'is-current': numDays === 7 }"
        class="action"
        @click.prevent="$emit('setNumDays', 7)"
      >
        7 Days
      </span>
      <span
        :class="{ 'is-current': numDays === 14 }"
        class="action"
        @click.prevent="$emit('setNumDays', 14)"
      >
        14 Days
      </span>
      <span
        :class="{ 'is-current': numDays === 28 }"
        class="action"
        @click.prevent="$emit('setNumDays', 28)"
      >
        28 Days
      </span>
      <span
        class="action"
        @click.prevent="$emit('reset')"
      >
        Reset
      </span>
      <span
        :class="{ 'is-current': snapMinutes === 15 }"
        class="action"
        @click.prevent="$emit('setSnapMinutes', 15)"
      >
        15
      </span>
      <span
        :class="{ 'is-current': snapMinutes === 30 }"
        class="action"
        @click.prevent="$emit('setSnapMinutes', 30)"
      >
        30
      </span>
      <color-chooser
        :width="(48)"
        :height="(22)"
        :colors="emissionColors"
        :selected-color="emissionColor"
        @select="$emit('setColor', $event)"
      />
      <span
        :class="{ 'is-current': isFullscreen }"
        class="action"
        @click.prevent="$emit('toggleFullscreen')"
      >
        FS
      </span>
    </div>

    <div class="calendar-navigation__right">
      <span
        class="action"
        @click.prevent="$emit('updateDaysOffset', -1)"
      >
        Day &#x3E;
      </span>
      <span
        class="action"
        @click.prevent="$emit('updateDaysOffset', -7)"
      >
        Week &#x3E;
      </span>
    </div>
  </div>
</template>
