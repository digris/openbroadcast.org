<script>

    const DEBUG = false;
    const NEARBY_HOURS = 48;
    const DAY_START_HOUR = 6;
    const DAYS_BACK = 21;
    const DAYS_ADVANCE = 7;

    const DAYPART_MARKERS = [6, 8, 11, 12, 16, 18, 19, 22, 23];

    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import utc from 'dayjs/plugin/utc'
    import weekday from 'dayjs/plugin/weekday';
    import {templateFilters} from '../../utils/template-filters';

    dayjs.extend(toObject);
    dayjs.extend(utc);
    dayjs.extend(weekday);


    const getDayRange = function () {
        const days = [];
        const today = dayjs(new Date()).hour(DAY_START_HOUR).minute(0).second(0).millisecond(0);
        for (let i = DAYS_BACK * -1; i < DAYS_ADVANCE; i++) {
            const timeStart = today.add(i, 'day');
            days.push({
                timeStart: timeStart,
                weekday: timeStart.weekday(),
                isWeekend: (timeStart.weekday() === 0 || timeStart.weekday() === 6),
                isToday: timeStart.isSame(today, 'day'),
                dayName: timeStart.format('dd')
            })
        }
        return days;
    };

    const checkIfSlotInDaypart = function(timeStart, timeEnd, dayparts) {
        // console.debug('checkIfSlotInDaypart', timeStart, dayparts);
        // dayjs starts with 0 on sunday, we start with 0 on monday...
        const dayMap = [6, 0, 1, 2, 3, 4, 5];
        const dayNumber = dayMap[timeStart.day()];
        const daypartsForDay = dayparts.filter(daypart => daypart.day === dayNumber);

        if(daypartsForDay.length < 1) {
            return false;
        }

        const slotHourStart = timeStart.hour();
        const slotHourEnd = (timeEnd.hour() === 0) ? 24 : timeEnd.hour();

        return daypartsForDay.some((daypart) => {

            let daypartHourStart = parseInt(daypart.start.substr(0,2));
            let daypartHourEnd = parseInt(daypart.end.substr(0,2));

            daypartHourStart = (daypartHourStart === 24) ? 0 : daypartHourStart;
            daypartHourEnd = (daypartHourEnd === 0) ? 24 : daypartHourEnd;

            if((slotHourStart >= daypartHourStart) && (slotHourEnd <= daypartHourEnd)) {
                return true;
            }
        });


    };

    export default {
        name: 'EmissionHistoryMatrix',
        filters: templateFilters,
        props: {
            emissionHistory: {
                type: Array,
                required: false,
                default: function () {
                    return [];
                },
            },
            objUuid: {
                type: String,
                required: true,
            },
            theme: {
                type: String,
                default: 'light',
                validator: function (value) {
                    return ['dark', 'light'].indexOf(value) !== -1;
                }
            },
        },
        computed: {
            days() {
                const days = getDayRange();

                days.forEach((day) => {
                    day.slots = this.getSlotsForDay(day);
                });

                // days.map(day => this.annotateWithEmissions(day));

                return days;
            },
            legend() {
                return this.getLegend();
            },
            playlist() {
                return this.$store.getters['library/playlistsByUuid'](this.objUuid);
            },
        },
        mounted: function () {
            this.$store.dispatch('library/loadPlaylist', {uuid: this.objUuid});
        },
        methods: {
            getEmissionsForRange: function (timeStart, timeEnd) {

                // add offset to catch short or overlapping entries
                timeStart = timeStart.add(3570, 'second');
                timeEnd = timeEnd.subtract(3570, 'second');

                return this.emissionHistory.filter((emission) => {
                    return (dayjs(emission.timeStart).isBefore(timeStart) && dayjs(emission.timeEnd).isAfter(timeEnd))
                });
            },
            getSlotsForDay: function (day) {
                // const now = dayjs(new Date());
                const slots = [];
                for (let i = 0; i < 24; i++) {
                    const timeStart = day.timeStart.add(i, 'hour');
                    const timeEnd = day.timeStart.add(i + 1, 'hour');
                    const emissions = this.getEmissionsForRange(timeStart, timeEnd);
                    slots.push({
                        timeStart: timeStart,
                        timeEnd: timeEnd,
                        emissions: emissions,
                        // hasWarning: emissions.length > 0 && Math.abs(timeStart.diff(now, 'hour')) < NEARBY_HOURS,
                        hasDaypartMarker: DAYPART_MARKERS.includes(timeStart.$H),
                        // hasDaypartMatch: (this.playlist && this.playlist.dayparts.length === 5),
                        hasDaypartMatch: (this.playlist) ? checkIfSlotInDaypart(timeStart, timeEnd, this.playlist.dayparts) : false
                    })
                }
                return slots;
            },
            getLegend: function () {
                const day = dayjs(new Date()).utc().hour(DAY_START_HOUR).minute(0).second(0).millisecond(0);
                const slots = [];
                // const daypartMarkers = [1,2,3,4,5,6]
                for (let i = 0; i < 24; i++) {
                    const timeStart = day.add(i, 'hour');
                    const timeEnd = day.add(i + 1, 'hour');

                    slots.push({
                        timeStart: timeStart,
                        // label: `${timeStart.format('HH')} - ${timeEnd.format('HH')}`,
                        label: `${timeStart.format('H')}h`,
                        hasDaypartMarker: DAYPART_MARKERS.includes(timeStart.$H)
                    })
                }
                return slots;
            }
        }
    }
</script>
<style lang="scss" scoped>

    .emission-history {

        // border: 10px solid greenyellow;

        --slot-height: 16px;

        //--border-color: #c9c9c9;
        //--border-color-light: #efefef;

        --border-color: #00000030;
        --border-color-light: #00000007;

        --slot-with-emission-color: #00000090;
        --daypart-match-bg-color: #03c95425;
        --today-bg-color: #B33FC925;
        --weekend-bg-color: #00000010;

        &--dark {

            --border-color: #FFFFFF30;
            --border-color-light: #FFFFFF07;
            --slot-with-emission-color: #FFFFFF90;

        }


        .grid {

            cursor: pointer;


            font-size: 90%;

            display: grid;
            grid-template-rows: 20px auto;
            grid-template-columns: 30px auto;
            grid-template-areas: "dayparts header" "dayparts matrix";

            &__dayparts {
                grid-area: dayparts;
                margin-top: 20px;
                width: 100%;
                // background: var(--border-color);


                &__slot {
                    height: var(--slot-height);

                    display: flex;
                    justify-content: flex-end;
                    align-items: center;
                    padding-right: 6px;

                    /*border-bottom: 1px solid var(--border-color-light);*/
                    /*&:first-child {*/
                    /*    border-top: 1px solid var(--border-color);*/
                    /*}*/

                    &.has-daypart-marker {
                        border-bottom-color: var(--border-color);
                    }

                }

            }

            &__header {
                grid-area: header;
                height: 20px;

                display: grid;
                grid-template-columns: repeat(28, 1fr);

                &__day {
                    /*border-right: 1px solid var(--border-color);*/
                    /*&:first-child {*/
                    /*    border-left: 1px solid var(--border-color);*/
                    /*}*/

                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

            }

            &__matrix {

                grid-area: matrix;
                width: 100%;
                display: grid;
                grid-template-columns: repeat(28, 1fr);
                cursor: crosshair;

                &__day {
                    border-right: 1px solid var(--border-color);

                    &:first-child {
                        border-left: 1px solid var(--border-color);
                    }

                    &.is-weekend {
                        background: var(--weekend-bg-color);
                    }

                    &.is-today {
                        background: var(--today-bg-color);
                    }

                }

                &__slot {
                    height: var(--slot-height);
                    border-bottom: 1px solid var(--border-color-light);

                    &:first-child {
                        border-top: 1px solid var(--border-color);
                    }

                    &.has-daypart-marker {
                        // draw stronger line to distinct dayparts
                        border-bottom-color: var(--border-color);
                    }

                    &.has-daypart-match {
                        background: var(--daypart-match-bg-color);
                    }

                    &.has-emission {
                        // background: var(--slot-with-emission-color);
                    }

                    &__emission {
                        width: 100%;
                        height: 100%;
                        background: var(--slot-with-emission-color);
                    }

                }

            }

        }
    }


</style>

<template>
  <div
    class="emission-history"
    :class="{ 'emission-history--dark': (theme === 'dark') }"
  >
    <div class="grid">
      <div class="grid__dayparts">
        <div
          v-for="(slot, index) in legend"
          :key="`slot-${index}`"
          class="grid__dayparts__slot"
          :class="{ 'has-daypart-marker': slot.hasDaypartMarker }"
        >
          <span v-if="slot.hasDaypartMarker">{{ slot.label }}</span>
        </div>
      </div>

      <div class="grid__header">
        <div
          v-for="(day, index) in days"
          :key="`day-${index}`"
          class="grid__header__day"
          :class="{ 'is-weekend': day.isWeekend, 'is-today': day.isToday }"
        >
          {{ day.dayName }}
        </div>
      </div>

      <div class="grid__matrix">
        <div
          v-for="(day, dayIndex) in days"
          :key="`day-${dayIndex}`"
          class="grid__matrix__day"
          :class="{ 'is-weekend': day.isWeekend, 'is-today': day.isToday }"
        >
          <div
            v-for="(slot, slotIndex) in day.slots"
            :key="`day-slot-${slotIndex}`"
            class="grid__matrix__slot"
            :class="{ 'has-emission': slot.emissions.length, 'has-daypart-marker': slot.hasDaypartMarker, 'has-daypart-match': slot.hasDaypartMatch }"
          >
            <div
              v-if="( slot.emissions.length)"
              class="grid__matrix__slot__emission"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
