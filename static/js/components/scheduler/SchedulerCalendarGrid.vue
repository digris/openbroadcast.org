<script>
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

        props: {
            days: Array,
            pixelHeightPerHour: Number,
        },
        methods: {},
        computed: {
            timeGrid() {
                const rows = [];
                for(let i = 0; i < 48; i++) {
                    rows.push({
                        index: i,
                        top: this.pixelHeightPerHour / 2 * i
                    })
                }
                return rows;
            },
            daypartGrid() {
                const dayparts = [];
                DAYPARTS.forEach((dp) => {
                    dayparts.push({
                        label: dp.label,
                        height: this.pixelHeightPerHour * dp.hours,
                        top: this.pixelHeightPerHour * dp.start
                    })
                });
                return dayparts;
            },
        }
    }
</script>
<style lang="scss" scoped>

    $border-color: #dadada;
    $border-dark-color: #a5a5a5;

    .scheduler-grid {
        position: relative;
        height: 100%;
        &__row {
            position: absolute;
            width: calc(100% - 61px);
            margin-left: 61px;
            border-bottom: 1px solid $border-color;
            &:nth-child(even) {
                border-bottom-style: dotted;
                border-bottom-color: rgba($border-color, .4);
            }
        }
        &__dayparts {
            height: calc(100% - 50px);
            position: absolute;
            width: 100%;
            margin-top: 50px;
            display: flex;
            flex-direction: column;
            border: 1px solid $border-color;
            &__daypart {
                width: 100%;
                border-bottom: 1px solid $border-dark-color;
                position: absolute;

                &:last-child {
                    border-bottom: 0;
                }

                .daypart-label {
                    width: 61px;
                    text-align: right;
                    padding: 4px 4px 0 0;
                    color: #333;
                    display: inline-block;
                }
            }
        }
        &__days {
            // background: blue;
            height: 100%;
            margin-left: 61px;
            display: flex;
            &__day {

                height: 100%;
                flex-grow: 1;
                .day-header {
                    height: 50px;
                    display: flex;
                    justify-content: center;
                    padding: 6px 0 0 0;

                    .day-label {
                        display: inline-block;
                        width: 30px;
                    }
                }

                .day-column {
                    height: calc(100% - 50px);
                    border-left: 1px solid $border-color;
                }

                &.is-weekend {
                    .day-column {
                        background: rgba(3, 3, 3, 0.04);
                    }
                }

                &.is-today {

                    border-top: 1px solid $border-color;
                    b// ackground: rgba(3, 201, 84, 0.12);

                    .day-header {
                        // font-weight: 400;
                    }

                    .day-column {
                        // background: rgba(3, 201, 84, 0.12);
                    }
                }
            }
        }
    }
</style>

<template>
    <div
        class="scheduler-grid">
            <div
                class="scheduler-grid__row"
                :style="{ top: row.top + 50 + 'px' }"
                v-for="(row, index) in timeGrid"
                :key="`grid-row-${index}`"></div>

            <div class="scheduler-grid__dayparts">
                <div
                    class="scheduler-grid__dayparts__daypart"
                    :style="{ top: daypart.top + 'px', height: daypart.height + 'px' }"
                    v-for="(daypart, index) in daypartGrid"
                    :key="`grid-daypart-${index}`">
                    <span
                        class="daypart-label">{{ daypart.label }}</span>
                </div>
            </div>

            <div class="scheduler-grid__days">
                <div
                    v-for="(day, index) in days"
                    :key="`day-row-${index}`"
                    :class="{ 'is-weekend': day.isWeekend, 'is-today': day.isToday }"
                    class="scheduler-grid__days__day">
                    <div
                        class="day-header">
                        <span class="day-label">{{ day.dayName }}</span>
                    </div>
                    <div
                        class="day-column"></div>
                </div>
            </div>
    </div>
</template>
