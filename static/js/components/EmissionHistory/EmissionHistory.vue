<script>

import ClickOutside from 'vue-click-outside';
import dayjs from 'dayjs';
import toObject from 'dayjs/plugin/toObject';
import relativeTime from 'dayjs/plugin/relativeTime';

import EmissionHistoryMatrix from './EmissionHistoryMatrix.vue';

const DEBUG = false;
const NEARBY_HOURS = 48;

dayjs.extend(toObject);
dayjs.extend(relativeTime);

export default {
  name: 'EmissionHistory',
  components: {
    matrix: EmissionHistoryMatrix,
  },
  directives: {
    ClickOutside,
  },
  filters: {
    // dateTime: function (value) {
    //     if (!value) return '';
    //     console.debug(value, dayjs(value).format('DD/MM/YYYY'));
    //     return dayjs(value).format('DD/MM/YYYY');
    // },
    relativeDateTime(value) {
      if (!value) return '';
      return dayjs(value).fromNow();
    },
  },
  props: {
    objCt: {
      type: String,
      required: true,
    },
    objUuid: {
      type: String,
      required: true,
    },
    hasWarning: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      nearbyEmissionsVisible: false,
      matrixVisible: false,
    };
  },
  computed: {
    emissionHistory() {
      return this.$store.getters['objectHistory/objectHistoryByKey'](this.objCt, this.objUuid);
    },

    pastEmissions() {
      const now = dayjs(new Date());
      return this.emissionHistory.filter((emission) => dayjs(emission.timeStart).isBefore(now));
    },

    upcomingEmissions() {
      const now = dayjs(new Date());
      return this.emissionHistory.filter((emission) => dayjs(emission.timeStart).isAfter(now));
    },

    lastEmission() {
      if (this.pastEmissions && this.pastEmissions.length > 0) {
        return this.pastEmissions[0];
      }
      return null;
    },
    lastEmissionWarning() {
      if (!this.lastEmission) {
        return null;
      }
      const now = dayjs(new Date());
      const time = dayjs(this.lastEmission.timeStart);
      return Math.abs(time.diff(now, 'hour')) < NEARBY_HOURS;
    },
    nextEmission() {
      if (this.upcomingEmissions && this.upcomingEmissions.length > 0) {
        return this.upcomingEmissions.slice(-1)[0];
      }
      return null;
    },
    nextEmissionWarning() {
      if (!this.nextEmission) {
        return null;
      }
      const now = dayjs(new Date());
      const time = dayjs(this.nextEmission.timeStart);
      return Math.abs(time.diff(now, 'hour')) < NEARBY_HOURS;
    },
  },
  mounted() {

  },
  methods: {
    loadHistory(e) {
      this.$store.dispatch('objectHistory/loadObjectHistory', { objCt: this.objCt, objUuid: this.objUuid });
    },
    showNearbyEmissions(e) {
      if (!this.emissionHistory) {
        this.loadHistory();
        console.log('history not loaded - trigger!');
      }
      this.nearbyEmissionsVisible = true;
    },
    hideNearbyEmissions(e) {
      this.nearbyEmissionsVisible = false;
    },
    toggleMatrix(e) {
      if (!this.matrixVisible) {
        this.showMatrix();
      } else {
        this.hideMatrix();
      }
    },
    showMatrix() {
      this.loadHistory();
      this.matrixVisible = true;
    },
    hideMatrix() {
      this.matrixVisible = false;
    },
  },
};
</script>
<style lang="scss" scoped>
    .emission-history {
      $self: &;

      position: relative;

      &__indicator {
        position: absolute;
        right: 0;
        display: inline-flex;
        justify-content: center;
        width: 21px;
        height: 21px;
        font-weight: 400;
        background: white;
        cursor: pointer;
      }

      &--has-warning {
        background: deepskyblue;

        #{ $self }__indicator {
          color: white;
          background: orangered;
        }
      }

      &__nearby-emissions {
        position: absolute;
        top: 21px;
        right: 0;
        width: 197px;
        background: white;

        > div {
          margin: 1px 0;
          padding: 2px 6px;
          background: rgba(50, 205, 50, 0.15);
          border-left: 4px solid limegreen;

          &.has-warning {
            color: orangered;
            font-weight: 400;
            background: rgba(255, 69, 0, 0.15);
            // background: red;
            border-left: 4px solid orangered;
          }
        }
      }

      &__matrix-container {
        position: absolute;
        top: 21px;
        z-index: 999;
        min-width: 640px;
        background: white;
        border: 1px solid #bcbcbc;
        box-shadow: 2px 2px 2px 1px rgba(0, 0, 0, 0.05);
        transform: translateX(-50%);
      }
    }
</style>

<template>
  <div
    v-click-outside="hideMatrix"
    :class="{ 'emission-history--has-warning': hasWarning }"
    class="emission-history"
  >
    <div
      class="emission-history__indicator"
      @mouseover="showNearbyEmissions"
      @mouseleave="hideNearbyEmissions"
      @click="toggleMatrix"
    >
      <span>H</span>
    </div>
    <div
      v-if="nearbyEmissionsVisible"
      class="emission-history__nearby-emissions"
    >
      <div
        :class="{ 'has-warning': lastEmissionWarning }"
      >
        <span>Last emission</span>
        <ul>
          <li
            v-if="lastEmission"
          >
            {{ lastEmission.timeStart | relativeDateTime }}
          </li>
          <li
            v-else
          >
            No emissions yet
          </li>
        </ul>
      </div>
      <div
        :class="{ 'has-warning': nextEmissionWarning }"
      >
        <span>Next emission</span>
        <ul>
          <li
            v-if="nextEmission"
          >
            {{ nextEmission.timeStart | relativeDateTime }}
          </li>
          <li
            v-else
          >
            No emission scheduled
          </li>
        </ul>
      </div>
    </div>
    <div
      v-if="matrixVisible"
      class="emission-history__matrix-container"
    >
      <matrix
        :obj-uuid="objUuid"
        :emission-history="emissionHistory"
      />
    </div>
  </div>
</template>
