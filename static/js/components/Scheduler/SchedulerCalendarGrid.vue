<script>
import { templateFilters } from 'src/utils/template-filters';

const DEBUG = false;

const DAYPARTS = [
  {
    label: '06 - 07',
    start: 0,
    hours: 1,
  },
  {
    label: '07 - 09',
    start: 1,
    hours: 2,
  },
  {
    label: '09 - 12',
    start: 3,
    hours: 3,
  },
  {
    label: '12 - 13',
    start: 6,
    hours: 1,
  },
  {
    label: '13 - 16',
    start: 7,
    hours: 3,
  },
  {
    label: '16 - 19',
    start: 10,
    hours: 3,
  },
  {
    label: '19 - 20',
    start: 13,
    hours: 1,
  },
  {
    label: '20 - 23',
    start: 14,
    hours: 3,
  },
  {
    label: '23 - 24',
    start: 17,
    hours: 1,
  },
  {
    label: '24 - 06',
    start: 18,
    hours: 6,
  },
];

export default {
  name: 'SchedulerCalendarGrid',
  filters: templateFilters,
  props: {
    days: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
    pixelHeightPerHour: {
      type: Number,
      required: true,
    },
  },
  computed: {
    timeGrid() {
      const rows = [];
      for (let i = 0; i < 48; i++) {
        rows.push({
          index: i,
          top: this.pixelHeightPerHour / 2 * i,
        });
      }
      return rows;
    },
    daypartGrid() {
      const dayparts = [];
      DAYPARTS.forEach((dp) => {
        dayparts.push({
          label: dp.label,
          height: this.pixelHeightPerHour * dp.hours,
          top: this.pixelHeightPerHour * dp.start,
        });
      });
      return dayparts;
    },
    numDays() {
      return this.days.length;
    },
  },
  methods: {},
};
</script>

<template>
  <div
    class="scheduler-grid"
  >
    <div
      v-for="(row, index) in timeGrid"
      :key="`grid-row-${index}`"
      class="scheduler-grid__row"
      :style="{ top: row.top + 50 + 'px' }"
    />

    <div class="scheduler-grid__dayparts">
      <div
        v-for="(daypart, index) in daypartGrid"
        :key="`grid-daypart-${index}`"
        class="scheduler-grid__dayparts__daypart"
        :style="{ top: daypart.top + 'px', height: daypart.height + 'px' }"
      >
        <span
          class="daypart-label"
        >{{ daypart.label }}</span>
      </div>
    </div>

    <div class="scheduler-grid__days">
      <div
        class="scheduler-grid__days__placeholder_hack"
      />

      <div
        v-for="(day, index) in days"
        :key="`day-row-${index}`"
        :class="{ 'is-weekend': day.isWeekend, 'is-today': day.isToday }"
        class="scheduler-grid__days__day"
      >
        <div
          class="day-header"
          :class="{ 'day-header--small': (numDays > 14) }"
        >
          <span
            class="day-label"
          >{{ day.dayName }}</span>
          <span
            class="day-date"
          >{{ day.timeStart|date('D.') }}</span>
        </div>
        <div
          class="day-column"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>

  $border-color: #dadada;
  $border-dark-color: #a5a5a5;
  $background-color: #fff;

  .scheduler-grid {
    position: relative;

    height: 100%;

    background: $background-color;

    &__row {
      position: absolute;

      width: calc(100% - 61px);
      margin-left: 61px;

      border-bottom: 1px solid $border-color;

      &:nth-child(even) {
        border-bottom-color: rgba($border-color, 0.4);
        border-bottom-style: dotted;
      }
    }

    &__dayparts {
      position: absolute;

      display: flex;
      flex-direction: column;
      width: 100%;
      height: calc(100% - 50px);
      margin-top: 50px;

      border: 1px solid $border-color;

      &__daypart {
        position: absolute;

        width: 100%;

        border-bottom: 1px solid $border-dark-color;

        &:last-child {
          border-bottom: 0;
        }

        .daypart-label {
          display: inline-block;
          width: 61px;
          padding: 4px 4px 0 0;

          color: #333;
          text-align: right;
        }
      }
    }

    &__days {
      // margin-left: 61px;
      display: flex;
      // background: blue;
      height: 100%;

      &__placeholder_hack {
        width: 61px;
        height: 50px;

        background: #f5f5f5;
      }

      &__day {
        flex-grow: 1;
        height: 100%;

        .day-header {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 50px;
          padding: 6px 0 0 0;

          background: #f5f5f5;

          .day-label {
            display: inline-block;
            width: 30px;

            text-align: center;
          }

          .day-date {
            display: inline-block;
            width: 28px;
            margin-left: 2px;

            text-align: center;
          }

          &--small {
            font-size: 80%;

            .day-label,
            .day-date {
              width: 24px;
            }
          }
        }

        .day-column {
          height: calc(100% - 50px);

          background: $background-color;
          border-left: 1px solid $border-color;
        }

        &.is-weekend {
          .day-column {
            background: rgba(0, 0, 0, 0.025);
          }
        }

        &.is-today {

          .day-header {
            color: orangered;
            font-weight: 400;
          }

        }
      }
    }
  }
</style>
