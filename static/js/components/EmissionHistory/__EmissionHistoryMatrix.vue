<script>

    const DEBUG = false;
    const NEARBY_HOURS = 48;
    const DAY_START_HOUR = 6;
    const DAYS_BACK = 21;
    const DAYS_ADVANCE = 7;

    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import utc from 'dayjs/plugin/utc'
    import weekday from 'dayjs/plugin/weekday';

    dayjs.extend(toObject);
    dayjs.extend(utc);
    dayjs.extend(weekday);


    const getDayRange = function() {
        const days = [];
        const today = dayjs(new Date()).hour(DAY_START_HOUR).minute(0).second(0).millisecond(0);
        for(let i=DAYS_BACK * -1; i < DAYS_ADVANCE; i++) {
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

    export default {
        name: 'EmissionHistoryMatrix',
        props: {
            emissionHistory: Array,
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
            }
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
            getSlotsForDay: function(day) {
                // const now = dayjs(new Date());
                const slots = [];
                for(let i = 0; i < 24; i++) {
                    const timeStart = day.timeStart.add(i, 'hour');
                    const timeEnd = day.timeStart.add(i + 1, 'hour');
                    const emissions = this.getEmissionsForRange(timeStart, timeEnd);
                    slots.push({
                        timeStart: timeStart,
                        timeEnd: timeEnd,
                        emissions: emissions,
                        // hasWarning: emissions.length > 0 && Math.abs(timeStart.diff(now, 'hour')) < NEARBY_HOURS
                    })
                }
                return slots;
            },
            getLegend: function() {
                const day = dayjs(new Date()).utc().hour(DAY_START_HOUR).minute(0).second(0).millisecond(0);
                const slots = [];
                // const daypartMarkers = [1,2,3,4,5,6]
                for(let i = 0; i < 24; i++) {
                    const timeStart = day.add(i, 'hour');
                    const timeEnd = day.add(i + 1, 'hour');

                    slots.push({
                        timeStart: timeStart,
                        label: `${timeStart.format('HH')} - ${timeEnd.format('HH')}`,
                        // hasDaypartMarker: daypartMarkers.includes(timeStart.$H)
                    })
                }
                return slots;
            }
        }
    }
</script>
<style lang="scss" scoped>

    $light-border-thin: #e9e9e9;
    $light-border: #d0d0d0;



    .emission-history {

        --border-color: blue;
        --border-color-light: orange;

        &--dark {

            --border-color: yellow;
            --border-color-light: yellow;

        }

        cursor: crosshair;
        .grid {
            display: flex;
            border-top: 1px solid var(--border-color-light);
            border-left: 1px solid var(--border-color-light);
            &__legend,
            &__day {
                border-right: 1px solid var(--border-color-light);
                &__header {
                    border-bottom: 1px solid var(--border-color);
                    text-align: center;
                }

                &__slot {
                    height: 16px;
                    border-bottom: 1px solid var(--border-color-light);

                    &:nth-child(2),
                    &:nth-child(4),
                    &:nth-child(7),
                    &:nth-child(8),
                    &:nth-child(11),
                    &:nth-child(14),
                    &:nth-child(15),
                    &:nth-child(18),
                    &:nth-child(19)
                    {
                        border-bottom-color: var(--border-color);
                    }
                }
            }

            &__legend {
                &__slot {
                    font-size: 90%;
                    width: 40px;
                    padding-right: 4px;
                    text-align: right;
                }
            }

            &__day {
                flex-grow: 1;

                &.is-weekend {
                    background: rgba(3, 3, 3, 0.1)
                }

                &.is-today {
                    background: rgba(3, 201, 84, 0.12);
                }

                &__slot {
                    &.has-emission {
                        background: #000;
                    }
                }
            }
        }
    }




</style>

<template>
    <div
        class="emission-history"
        :class="{ 'emission-history--dark': (theme === 'dark') }">

        <div class="grid">
            <div
                class="grid__legend">
                <div
                    class="grid__legend__header">
                    &nbsp;
                </div>
                <div
                    class="grid__legend__slot"
                    v-for="(slot, index) in legend"
                    :key="`slot-${index}`">
                    {{ slot.label }}
                </div>
            </div>
            <div
                class="grid__day"
                :class="{ 'is-weekend': day.isWeekend,  'is-today': day.isToday }"
                v-for="(day, index) in days"
                :key="`day-${index}`">
                <div
                    class="grid__day__header">
                    {{ day.dayName }}
                </div>
                <div
                    class="grid__day__slot"
                    :class="{ 'has-emission': slot.emissions.length }"
                    v-for="(slot, index) in day.slots"
                    :key="`day-slot-${index}`">
                </div>
            </div>
        </div>
    </div>
</template>
