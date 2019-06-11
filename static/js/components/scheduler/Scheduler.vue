<script>

    const DEBUG = false;
    const NEARBY_HOURS = 48;
    const DAY_START_HOUR = 6;

    import ClickOutside from 'vue-click-outside';
    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import relativeTime from 'dayjs/plugin/relativeTime';

    import LayoutBase from '../../templates/LayoutBase.vue';
    import SchedulerCalendar from './SchedulerCalendar.vue';

    dayjs.extend(toObject);
    dayjs.extend(relativeTime);

    export default {
        name: 'Scheduler',
        components: {
            'layout-base': LayoutBase,
            'calendar': SchedulerCalendar,
        },
        directives: {

        },
        props: {
            channelUuid: String,
        },
        data() {
            return {
                timeStart: dayjs(new Date()).hour(DAY_START_HOUR).minute(0).second(0).millisecond(0),
                numDays: 7,
                daysOffset: 0,
            }
        },
        mounted: function () {

        },
        computed: {

        },
        methods: {

        },
    }
</script>
<style lang="scss" scoped>
    .content {
        background: yellow;
    }
</style>

<template>

    <layout-base>

        <template v-slot:default>
            <calendar
                :time-start="timeStart"
                :num-days="numDays"
                :days-offset="daysOffset"
            ></calendar>
            </template>

          <template v-slot:sidebar>
            <h1>Here might be a page title</h1>
          </template>

    </layout-base>
    <!--
    <div class="content">
        <div class="content__primary">
            (( P ))<br>
            {{ channelUuid }}
            <calendar
                :time-start="timeStart"
                :num-days="numDays"
                :days-offset="daysOffset"
            ></calendar>
        </div>
        <div class="content__sidebar">
             (( S ))
        </div>
    </div>
    -->
</template>
