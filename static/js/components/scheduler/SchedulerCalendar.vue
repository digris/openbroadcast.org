<script>

    const DEBUG = false;
    const NEARBY_HOURS = 48;
    const PPH = 48; // 'pixels per hour'

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

    import ClickOutside from 'vue-click-outside';
    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import relativeTime from 'dayjs/plugin/relativeTime';

    dayjs.extend(toObject);
    dayjs.extend(relativeTime);

    export default {
        name: 'SchedulerCalendar',
        components: {
            // 'matrix': EmissionHistoryMatrix,
        },
        directives: {

        },
        props: {
            timeStart: Object,
            numDays: Number,
            daysOffset: Number,
        },
        // data() {
        //     return {
        //         nearbyEmissionsVisible: false,
        //         matrixVisible: false,
        //     }
        // },
        mounted: function () {

        },
        computed: {
            timeGrid() {
                const rows = [];
                for(let i = 0; i < 48; i++) {
                    rows.push({
                        index: i,
                        top: PPH / 2 * i
                    })
                }
                return rows;
            },
            daypartGrid() {

                const dayparts = [];

                DAYPARTS.forEach((dp) => {
                    dayparts.push({
                        label: dp.label,
                        height: PPH * dp.hours,
                        top: PPH * dp.start
                    })
                });

                return dayparts;

            }
        },
        methods: {

        },
    }
</script>
<style lang="scss" scoped>
    .calendar {
        // background: orangered;

        .background-grid {
            position: relative;

            &__row {
                position: absolute;
                width: calc(100% - 80px);
                margin-left: 80px;
                border-bottom: 1px solid #dadada;
                &:nth-child(odd) {
                    border-bottom-style: dotted;
                }
            }

            &__daypart {
                position: absolute;
                width: 100%;
                border-bottom: 1px solid #ff00ff;
            }


        }

    }
</style>

<template>
    <div class="calendar">

        <div class="background-grid">

            <div
                class="background-grid__row"
                :style="{ top: row.top + 'px' }"
                v-for="row in timeGrid">
                <!--{{ row }}-->
            </div>

            <div
                class="background-grid__daypart"
                :style="{ top: daypart.top + 'px', height: daypart.height + 'px' }"
                v-for="daypart in daypartGrid">
                <span>{{ daypart.label }}</span>
            </div>



            <div class="background-grid__columns">

            </div>
        </div>

        <!--
        <div>
            {{ timeStart }}<br>
            {{ numDays }}<br>
            {{ daysOffset }}
        </div>
        -->

        <!--
        <div>
            dayparts
        </div>
        <div>
            day
        </div>
        -->
    </div>
</template>
