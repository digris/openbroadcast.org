<script>
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

export default {
  name: 'EmissionHistoryInline',
  components: {
    // date: Date,
  },
  filters: {
    date(value) {
      if (!value) return '';
      return dayjs(value).format('YYYY-MM-DD');
    },
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
  },
  data() {
    return {
      detailsVisible: false,
      loadingStarted: false,
    };
  },
  computed: {
    emissionHistory() {
      return this.$store.getters['objectHistory/objectHistoryByKey'](this.objCt, this.objUuid) || [];
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
    nextEmission() {
      if (this.upcomingEmissions && this.upcomingEmissions.length > 0) {
        return this.upcomingEmissions.slice(-1)[0];
      }
      return null;
    },
  },
  methods: {
    loadHistory() {
      if (!this.loadingStarted) {
        this.$store.dispatch('objectHistory/loadObjectHistory', { objCt: this.objCt, objUuid: this.objUuid });
        this.loadingStarted = true;
      }
    },
    showDetails() {
      this.loadHistory();
      this.detailsVisible = true;
    },
    hideDetails() {
      this.detailsVisible = false;
    },
  },
};
</script>

<template>
  <div
    class="emissions"
  >
    <div
      class="emissions__summary"
      @mouseover="showDetails"
      @mouseleave="hideDetails"
    >
      <span
        class="label"
      >History:</span>
      <span
        v-if="lastEmission"
        class="value"
      >{{ lastEmission.timeStart|date }}</span>
      <span
        v-else
        class="value value--blank"
      >-</span>
    </div>
    <div
      v-if="detailsVisible"
      class="emissions__details"
    >
      <div
        v-if="upcomingEmissions.length"
        class="emission-list emission-list--upcoming"
      >
        <div
          class="emission-list__title"
        >
          <span>Upcoming</span>
        </div>
        <div
          v-for="(emission, index) in upcomingEmissions"
          :key="`history-item-upcoming-${index}`"
          class="emission"
        >
          <span
            class="date--rel"
          >{{ emission.timeStart|relativeDateTime }}</span>
          <span
            class="date--abs"
          >{{ emission.timeStart|date }}</span>
        </div>
      </div>
      <div
        v-if="pastEmissions.length"
        class="emission-list emission-list--past"
      >
        <div
          class="emission-list__title"
        >
          <span>Past</span>
        </div>
        <div
          v-for="(emission, index) in pastEmissions"
          :key="`history-item-upcoming-${index}`"
          class="emission"
        >
          <span
            class="date--rel"
          >{{ emission.timeStart|relativeDateTime }}</span>
          <span
            class="date--abs"
          >{{ emission.timeStart|date }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.emissions {
  position: relative;
  &__summary {
    font-size: 90%;
    cursor: pointer;
    .label {
      color: #a3a3a3;
    }
  }
  &__details {
    position: absolute;
    right: 0;
    z-index: 1;
    min-width: 172px;
    padding: 0 0.5rem;
    background: #ffffff;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
  }
  .emission-list {
    &--upcoming {
      padding: 0.25rem;
    }
    &--past {
      padding: 0.25rem;
    }
    &__title {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 0.25rem;
      color: #a9a9a9;
    }
    .emission {
      display: flex;
      .date {
        &--rel {
          flex-grow: 1;
        }
      }
    }
  }
}
</style>
