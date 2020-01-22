<script>

import { Drag, Drop } from 'vue-drag-drop';
import throttle from 'lodash.throttle';
import uuid from 'uuid/v4';
import dayjs from 'dayjs';
import toObject from 'dayjs/plugin/toObject';
import relativeTime from 'dayjs/plugin/relativeTime';
import SchedulerCalendarEmission from './SchedulerCalendarEmission.vue';
import SchedulerCalendarEmissionPlaceholder from './SchedulerCalendarEmissionPlaceholder.vue';
import SchedulerCalendarEmissionEditor from './SchedulerCalendarEmissionEditor.vue';
import SchedulerCalendarGrid from './SchedulerCalendarGrid.vue';

const DEBUG = true;
const PPH = 48; // 'pixels per hour'
const SECONDS_PER_DAY = 60 * 60 * 24;

dayjs.extend(toObject);
dayjs.extend(relativeTime);

function quantizeNumber(val, quantum, { cover = false } = {}) {
  if (!quantum) {
    return 0;
  }
  const remainder = val % quantum;
  // I'm intentionally not using Math.sign so that no polyfill is
  // required to use this library in legacy environments.
  const sign = val >= 0 ? 1 : -1;
  const mod = cover && remainder ? quantum : 0;
  return val - remainder + sign * mod;
}

export default {
  name: 'SchedulerCalendar',
  components: {
    emission: SchedulerCalendarEmission,
    'emission-editor': SchedulerCalendarEmissionEditor,
    'emission-placeholder': SchedulerCalendarEmissionPlaceholder,
    grid: SchedulerCalendarGrid,
    drag: Drag,
    drop: Drop,
  },
  directives: {},
  props: {
    width: {
      type: Number,
      default: 0,
    },
    settings: {
      type: Object,
      default() {
        return {};
      },
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    days: {
      type: Array,
      default() {
        return [];
      },
    },
    emissions: {
      type: Object,
      default: null,
    },
    highlightObjUuid: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      // NOTE: "highlighted" vs "highlight"
      // `highlightObjUuid` is a prop and used to trigger highlighting from component "outside"
      highlightedObjUuid: null,

      draggedEmissionUuid: null,
      emissionPlaceholder: {
        visible: false,
        transferData: null,
        position: {
          x: 0,
          y: 0,
        },
      },
      calendarBounds: {
        x1: null,
        y1: null,
        x2: null,
        y2: null,
      },
      hasDragging: false,

      // 'cache' event cursor positions (raw & calculated)
      rawDragEventPosition: {
        x: null,
        y: null,
      },
      relativeDragEventPosition: {
        x: null,
        y: null,
      },
      errors: [],

      tempContainerRect: null,
      tempLastX: 0,
      tempLastY: 0,

      // emission editor
      emissionInEditorUuid: null,

      // current time display
      currentTime: null,
      currentTimeY: 0,
      currentTimeTimer: null,
    };
  },
  computed: {
    pixelHeightPerHour() {
      return this.settings.pixelHeightPerHour || PPH;
    },
    pixelHeightPerDay() {
      return this.pixelHeightPerHour * 24;
    },
    pixelWidthPerDay() {
      if (this.days && this.days.length > 0) {
        return (this.width - 61) / this.days.length;
      }
      return null;
    },
    dayStart() {
      if (this.days && this.days.length > 0) {
        return this.days[0];
      }
      return null;
    },
    calendarHeight() {
      return this.pixelHeightPerHour * 24;
    },
    mappedEmissions() {
      const emissions = [];

      for (const uuid in this.emissions) {
        const emission = this.emissions[uuid];
        const timeStart = emission.timeStartObj;

        // TODO: how to better handle DST ??
        // for now this atleast fixes the display. but maybe this should be handled in general...
        const UTCDiff = this.dayStart.timeStart.utcOffset() - timeStart.utcOffset();
        const timeDiff = timeStart.diff(this.dayStart.timeStart.add(UTCDiff, 'minute'), 'second');

        // exclude items out of displayed range
        if (timeDiff < 0 || timeDiff >= (60 * 60 * 24 * this.days.length)) {
          continue;
        }

        const position = this.timeDiffToPosition(timeDiff);
        emissions.push({
          obj: emission,
          timeDiff,
          name: emission.name,
          highlighted: emission.co.uuid === this.highlightedObjUuid,
          dragged: emission.uuid === this.draggedEmissionUuid,
          style: {
            left: `${position.x}px`,
            top: `${position.y}px`,
            height: `${emission.duration / 60 / 60 / 1000 * this.pixelHeightPerHour}px`,
            width: `${this.pixelWidthPerDay}px`,
          },
        });
      }
      return emissions;
    },

  },
  watch: {
    highlightObjUuid(uuid) {
      if (uuid) {
        this.highlightEmission(uuid, 1);
      } else {
        this.unhighlightEmission();
      }
    },
  },
  mounted() {
    const container = this.$refs.calendar;
    const node = container.getElementsByClassName('emissions')[0];
    const rect = node.getBoundingClientRect();

    // current time handler
    this.currentTimeTimer = setInterval(() => {
      const currentTime = dayjs();
      const dayStart = currentTime.hour(6).minute(0).second(0).millisecond(0);
      const timeDiff = currentTime.diff(dayStart, 'second');
      this.currentTimeY = Math.round(this.pixelHeightPerHour * timeDiff / 60 / 60) + 50;
      this.currentTime = currentTime;
    }, 1000);
  },
  methods: {

    // hover / highlight handling
    highlightEmission(uuid, minCount = 2) {
      if (this.readOnly) {
        return;
      }
      // check if object in emissions
      // to prevent unnecessary updates
      let count = 0;
      for (const k in this.emissions) {
        if (this.emissions[k].co.uuid === uuid) {
          count++;
        }
      }
      if (count >= minCount) {
        this.highlightedObjUuid = uuid;
      }
    },
    unhighlightEmission() {
      if (this.highlightedObjUuid) {
        this.highlightedObjUuid = null;
      }
    },

    // error handling
    addError(error) {
      console.warn('error', error.message, error.response);

      const errorMessage = {
        uuid: uuid(),
        messages: error.response.data || [error.message],
      };

      this.errors.unshift(errorMessage);
    },
    resetErrors() {
      this.errors = [];
    },

    // time- and offset calculations
    timeDiffToPosition(timeDiff) {
      const dayOffset = Math.floor(timeDiff / SECONDS_PER_DAY);
      const secondsOffset = timeDiff - (dayOffset * SECONDS_PER_DAY);

      // console.table(timeDiff, dayOffset, secondsOffset);

      return {
        x: this.pixelWidthPerDay * dayOffset,
        y: this.pixelHeightPerHour * secondsOffset / 60 / 60,
      };
    },
    positionToTimeDiff(position) {
      const dayOffset = position.x / this.pixelWidthPerDay;
      return (dayOffset * SECONDS_PER_DAY * 1000) + (position.y / this.pixelHeightPerHour) * 60 * 60 * 1000;
    },

    // drag event calculate positions
    eventToXY({ e, quantize = true, skipUnchanged = true }) {
      // check for changed position
      const rawPosition = this.rawDragEventPosition;
      if (skipUnchanged && rawPosition.x === e.clientX && rawPosition.y === e.clientY) {
        return null;
        // return this.relativeDragEventPosition;
      }
      rawPosition.x = e.clientX;
      rawPosition.y = e.clientY;


      // TODO: not s nice to always have to get the container/dimensions from DOM.
      // however, performance impact is close to zero...
      const container = this.$refs.calendar;
      const node = container.getElementsByClassName('emissions')[0];
      const rect = node.getBoundingClientRect();

      // calculate positions relative to container
      let x = e.clientX - rect.left;
      let y = e.clientY - rect.top;

      if (quantize) {
        x = quantizeNumber(x, this.pixelWidthPerDay);
        y = quantizeNumber(y, this.pixelHeightPerHour / (60 / this.settings.snapMinutes));
      }

      // console.debug('eventToXZ', 'r', x, y);

      const relativeePosition = {
        x,
        y,
      };

      this.relativeDragEventPosition = relativeePosition;

      return relativeePosition;
    },

    // drop events

    /**
             *
             */
    dragenter(transferData, e) {
      if (DEBUG) console.debug('dragenter', transferData, e);
      if (transferData.ct === 'abcast.emission') {
        this.draggedEmissionUuid = transferData.uuid;
      }
      this.hasDragging = true;
      this.emissionPlaceholder.transferData = transferData;
      this.emissionPlaceholder.visible = true;
    },
    dragleave(transferData, e) {
      if (DEBUG) console.debug('dragleave', transferData, e);
      if (transferData.ct === 'abcast.emission') {
        return;
      }
      this.hasDragging = false;
      this.emissionPlaceholder.visible = false;
    },


    dragover(transferData, e) {
      const position = this.eventToXY({ e });

      if (position) {
        // TODO: should not be needed!
        this.emissionPlaceholder.visible = true;
        this.emissionPlaceholder.position = position;
      }
    },
    drop(transferData, e) {
      const position = this.eventToXY({ e, skipUnchanged: false });
      const timeDiff = this.positionToTimeDiff(position);
      const timeStart = this.dayStart.timeStart.add(timeDiff, 'millisecond');
      const formattedTimeStart = timeStart.format('YYYY-MM-DD HH:mm');

      console.debug('drop', transferData, position, timeDiff, formattedTimeStart, e);

      // check if we have to update an existing emission or if
      // it is a copy resp. new item

      if (!e.altKey && transferData.ct === 'abcast.emission') {
        console.debug('reschedule emission');
        // this.updateEmission(transferData, formattedTimeStart);
        this.updateEmission(transferData, { time_start: formattedTimeStart });
      } else if (transferData.ct === 'abcast.emission') {
        console.debug('duplicated emission', transferData.co);
        this.createEmission(transferData.co, formattedTimeStart);
      } else {
        console.debug('added item to scheduler', transferData);
        this.createEmission(transferData, formattedTimeStart);
      }
    },

    emissionDrag: throttle((transferData, e) => {

      // if(e.x > 861) {
      //     console.debug('emissionDrag', 'x', e.x, 'y', e.y, e);
      //     this.$emit('updateDaysOffset', -1)
      // }
      //
      // if(e.x < 50) {
      //     console.debug('emissionDrag', 'x', e.x, 'y', e.y, e);
      //     this.$emit('updateDaysOffset', 1)
      // }

    }, 260),

    // handle changed position
    updateEmission(emission, payload) {
      // console.debug(emission);
      const dispatch = this.$store.dispatch('scheduler/updateEmission', {
        emission,
        payload,
      });
      dispatch.then((response) => {
        // console.log('ok', response);
        this.emissionPlaceholder.visible = false;
        // this.emissionPlaceholder.style = {};
        this.draggedEmissionUuid = null;
      }, (error) => {
        console.warn('error', error.message, error.response);

        this.addError(error);
        this.emissionPlaceholder.visible = false;
        this.draggedEmissionUuid = null;
      });
    },

    // handle changed position
    createEmission(contentObj, timeStart) {
      console.debug('createEmission', contentObj);
      const dispatch = this.$store.dispatch('scheduler/createEmission', {
        contentObj,
        timeStart,
        color: this.settings.emissionColor || 0,
      });
      dispatch.then((response) => {
        console.info('response', response);
        this.emissionPlaceholder.visible = false;
        this.draggedEmissionUuid = null;
      }, (error) => {
        console.warn('error', error.message, error.response);

        this.addError(error);
        this.emissionPlaceholder.visible = false;
        this.draggedEmissionUuid = null;

        // console.warn('error', error.message, error.response.data);
      });
    },

    // emission editor
    showEmissionEditor(uuid) {
      if (this.readOnly) {
        return;
      }
      this.emissionInEditorUuid = uuid;
    },
    closeEmissionEditor() {
      this.emissionInEditorUuid = null;
    },
  },
};
</script>
<style lang="scss" scoped>

    $border-color: #dadada;
    $border-dark-color: #a5a5a5;

    .calendar {
      position: relative;

      .emissions {
        position: absolute;
        top: 50px;
        left: 61px;

        width: calc(100% - 61px);
        height: 100%;

        .emission-container {
          position: absolute;

          background: #fff;
        }
      }

      .current-time {
        position: absolute;

        width: 100%;

        &__line {
          //background: orangered;
          height: 0;

          border-bottom: 1px dotted rgba(255, 69, 0, 0.5);
        }

        &__time {
          position: absolute;
          top: -5px;
          // left: -45px;
          left: -60px;

          color: orangered;
          font-size: 11px;
          line-height: 11px;
        }

        &__marker {
          position: absolute;
          top: 0;

          /* height: 10px; */

          /* width: 10px; */
          width: 0;
          height: 0;

          border-style: solid;
          transform: translate(0, -4.5px);

          &--left {
            left: -10px;

            border-color: transparent transparent transparent orangered;
            border-width: 5px 0 5px 8px;
          }

          &--right {
            right: -10px;

            border-color: transparent orangered transparent transparent;
            border-width: 5px 8px 5px 0;
          }
        }
      }

      .errors-container {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1001;

        width: 100%;
        height: 100%;

        background: rgba(26, 5, 0, 0.66);

        .errors {
          position: absolute;
          top: 50%;
          left: 50%;

          padding: 20px;

          color: white;

          background: orangered;
          transform: translate(-50%, -50%);

          .error {
            font-size: 120%;
            line-height: 180%;
            white-space: pre-line;
            text-align: left;
          }
        }
      }
    }

    .fade-in-out-enter-active {
      transition: opacity 200ms;
    }

    .fade-in-out-leave-active {
      transition: opacity 0.8ms;
    }

    .fade-in-out-enter,
    .fade-in-out-leave-to {
      opacity: 0;
    }

    .emission-list-leave-active {
      /* filter: grayscale(100%); */

      /* transition: opacity 2500ms; */
    }

    .emission-list-enter-active {
      transition: opacity 200ms;
    }

    .emission-list-enter,
    .emission-list-leave-to {
      opacity: 0;
    }

</style>

<template>
  <div
    ref="calendar"
    :style="{ height: calendarHeight + 50 + 'px' }"
    class="calendar"
  >
    <grid
      :pixel-height-per-hour="pixelHeightPerHour"
      :days="days"
    />

    <drop
      class="emissions"
      @dragenter="dragenter"
      @dragleave="dragleave"
      @dragover="dragover"
      @drop="drop"
    >
      <emission-placeholder
        :pixel-width-per-day="pixelWidthPerDay"
        :pixel-height-per-hour="pixelHeightPerHour"
        :placeholder="emissionPlaceholder"
      />

      <transition-group
        name="emission-list"
        tag="div"
      >
        <drag
          v-for="emission in mappedEmissions"
          :key="emission.obj.uuid"
          class="emission-container"
          :draggable="(! readOnly && ! emission.obj.hasLock)"
          :transfer-data="emission.obj"
          :style="emission.style"
          @drag="emissionDrag"
        >
          <template slot="image">
            <div><!-- empty drag handler --></div>
          </template>

          <emission
            :emission="emission"
            @dblclick="showEmissionEditor"
            @mouseover="highlightEmission"
            @mouseleave="unhighlightEmission"
          />
        </drag>
      </transition-group>
    </drop>

    <div
      v-if="currentTime"
      :style="{ top: currentTimeY + 'px'}"
      class="current-time"
    >
      <div
        class="current-time__time"
      >
        {{ currentTime.format('H:mm:s') }}
      </div>
      <div
        class="current-time__marker current-time__marker--left"
      />
      <div
        class="current-time__marker current-time__marker--right"
      />
      <div
        class="current-time__line"
      />
    </div>

    <transition
      name="fade-in-out"
    >
      <div
        v-if="(errors && errors.length)"
        class="errors-container"
        @click="resetErrors"
      >
        <div
          v-for="error in errors"
          :key="error.uuid"
          class="errors"
        >
          <p
            v-for="(message, index) in error.messages"
            :key="`error-message-${index}`"
            class="error"
          >
            {{ message }}
          </p>
        </div>
      </div>
    </transition>

    <h1>** {{ emissionInEditorUuid }} **</h1>

    <emission-editor
      :uuid="emissionInEditorUuid"
      @close="closeEmissionEditor"
    />

    <!--
        <div>
            bounds: {{ calendarBounds }}<br>
            ERRORS: {{ errors }}<br>
            HAS DRAGGING: {{ hasDragging }}<br>
            HIGHLIGHTED: {{ highlightedObjUuid }}<br>
            DRAG: {{ draggedEmissionUuid }}<br>
        </div>
        -->
  </div>
</template>
