<script>

    const DEBUG = false;
    const DAY_START_HOUR = 6;

    import debounce from 'debounce';
    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import utc from 'dayjs/plugin/utc'
    import weekday from 'dayjs/plugin/weekday';
    import advancedFormat from 'dayjs/plugin/advancedFormat';

    import LayoutBase from '../../templates/LayoutBase.vue';
    import SchedulerCalendarNavigation from './SchedulerCalendarNavigation.vue';
    import SchedulerCalendar from './SchedulerCalendar.vue';
    import SchedulerClipboard from './SchedulerClipboard.vue';

    dayjs.extend(toObject);
    dayjs.extend(relativeTime);
    dayjs.extend(utc);
    dayjs.extend(weekday);
    dayjs.extend(advancedFormat);

    export default {
        name: 'Scheduler',
        components: {
            'layout-base': LayoutBase,
            'calendar-navigation': SchedulerCalendarNavigation,
            'calendar': SchedulerCalendar,
            'clipboard': SchedulerClipboard,
        },
        directives: {},
        props: {
            channelUuid: String,
            readOnly: Boolean,
        },
        data() {
            return {
                calendarWidth: 0,
                dayRange: null,
                isFullscreen: false,
                highlightObjUuid: null,
            }
        },
        mounted: function () {
            this.$nextTick(() => {
               this.setSchedulerSizes();
            });
            // recalculate sizes on resize
            window.onresize = debounce(() => this.setSchedulerSizes(), 20);
            this.updateSchedule();
        },
        computed: {
            settings() {
                return this.$store.getters['scheduler/settings'];
            },
            emissions() {
                return this.$store.getters['scheduler/emissions'];
            },
            today() {
                return dayjs(new Date()).hour(DAY_START_HOUR).minute(0).second(0).millisecond(0);
            },
            offset() {
                return this.today.day() - 1 + this.settings.daysOffset;
            },
            dayStart() {
                if (this.days && this.days.length > 0) {
                    return this.days[0];
                }
                return null;
            },
            dayEnd() {
                if (this.days && this.days.length > 0) {
                    return this.days.slice(-1)[0];
                }
                return null;
            },
            days() {
                const days = [];
                for (let i = 0; i < this.settings.numDays; i++) {
                    const offset = i - this.offset;
                    const timeStart = this.today.add(offset, 'day');
                    days.push({
                        timeStart: timeStart,
                        timeEnd: timeStart.hour(23).minute(59).second(59),
                        isWeekend: [0, 6].includes(timeStart.weekday()),
                        isToday: timeStart.isSame(this.today, 'day'),
                        dayName: timeStart.format('dd'),
                    })
                }
                return days;
            }
        },
        methods: {
            setSchedulerSizes: function() {
                const calendarContainer = this.$refs['calendar'];
                const rect = calendarContainer.$el.getBoundingClientRect();
                const calendarWidth = rect.width;
                this.calendarWidth = calendarWidth;
            },
            updatePixelHeightPerHour: function(value) {
                let settings = Object.assign({}, this.settings);
                settings.pixelHeightPerHour += value;
                this.updateSettings(settings);
            },
            updateDaysOffset: function (offset) {
                let settings = Object.assign({}, this.settings);
                settings.daysOffset += offset;
                this.updateSettings(settings);
            },
            setNumDays: function (numDays) {
                let settings = Object.assign({}, this.settings);
                settings.numDays = numDays;
                this.updateSettings(settings);
            },
            setSnapMinutes: function (snapMinutes) {
                let settings = Object.assign({}, this.settings);
                settings.snapMinutes = snapMinutes;
                this.updateSettings(settings);
            },
            setColor: function (color) {
                let settings = Object.assign({}, this.settings);
                settings.emissionColor = parseInt(color);
                this.updateSettings(settings);
            },
            updateSettings: function (settings) {
                this.$store.dispatch('scheduler/setSettings', settings);
            },
            setDefaultSettings: function () {
                this.$store.dispatch('scheduler/setDefaultSettings');
            },
            updateSchedule: function () {
                const timeStart = this.dayStart.timeStart.format('YYYY-MM-DD HH:mm');
                const timeEnd = this.dayEnd.timeEnd.add(6, 'hour').format('YYYY-MM-DD HH:mm');
                this.$store.dispatch('scheduler/loadSchedule', {timeStart: timeStart, timeEnd: timeEnd});
            },
            debouncedUpdateSchedule: debounce(function () {
                console.debug('debounced updateSchedule');
                this.updateSchedule();
            }, 250),
            // TODO: check implementation
            clipboardItemMouseenter: function(uuid) {
                this.highlightObjUuid = uuid;
            },
            clipboardItemMouseleave: function(uuid) {
                this.highlightObjUuid = null;
            },
        },
        watch: {
            settings: function (o, n) {
                this.debouncedUpdateSchedule();
            },
            isFullscreen: function (o, n) {
                this.$nextTick(() => {
                   this.setSchedulerSizes();
                });

            },
        },
    }
</script>

<style lang="scss" scoped>
    .calendar-navigation {
        margin-bottom: 24px;
    }
</style>

<template>
    <layout-base
        :fullscreen="isFullscreen">
        <calendar-navigation
            :settings="settings"
            :isFullscreen="isFullscreen"
            @toggleFullscreen="isFullscreen = !isFullscreen"
            @updateDaysOffset="updateDaysOffset"
            @setNumDays="setNumDays"
            @decreaseVerticalSize="updatePixelHeightPerHour(-6)"
            @increaseVerticalSize="updatePixelHeightPerHour(6)"
            @setSnapMinutes="setSnapMinutes"
            @setColor="setColor"
            @reset="setDefaultSettings"></calendar-navigation>
        <calendar
            ref="calendar"
            :channel-uuid="channelUuid"
            :read-only="readOnly"
            :width="calendarWidth"
            :settings="settings"
            :emissions="emissions"
            :days="days"
            :highlightObjUuid="highlightObjUuid"
            @updateDaysOffset="updateDaysOffset"
        ></calendar>
        <template v-slot:sidebar>
            <clipboard
                style="margin-top: 89px;"
                v-if="(! readOnly)"
                @itemMouseenter="clipboardItemMouseenter"
                @itemMouseleave="clipboardItemMouseleave"></clipboard>
        </template>
    </layout-base>
</template>
