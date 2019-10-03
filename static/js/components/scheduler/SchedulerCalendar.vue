<script>

    const DEBUG = true;
    const PPH = 48; // 'pixels per hour'
    const SECONDS_PER_DAY = 60 * 60 * 24;


    import {Drag, Drop} from 'vue-drag-drop';
    import throttle from 'lodash.throttle';
    import uuid from 'uuid/v4';
    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import SchedulerCalendarEmission from './SchedulerCalendarEmission.vue';
    import SchedulerCalendarEmissionPlaceholder from './SchedulerCalendarEmissionPlaceholder.vue';
    import SchedulerCalendarEmissionEditor from './SchedulerCalendarEmissionEditor.vue';
    import SchedulerCalendarGrid from './SchedulerCalendarGrid.vue';

    dayjs.extend(toObject);
    dayjs.extend(relativeTime);

    function quantizeNumber(val, quantum, {cover = false} = {}) {
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
            'emission': SchedulerCalendarEmission,
            'emission-editor': SchedulerCalendarEmissionEditor,
            'emission-placeholder': SchedulerCalendarEmissionPlaceholder,
            'grid': SchedulerCalendarGrid,
            'drag': Drag,
            'drop': Drop,
        },
        directives: {},
        props: {
            width: Number,
            settings: Object,
            channelUuid: String,
            readOnly: Boolean,
            days: Array,
            emissions: Object,
            highlightObjUuid: String,
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
                        y: 0
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
            }
        },
        mounted: function () {

            const container = this.$refs['calendar'];
            const node = container.getElementsByClassName("emissions")[0];
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
                return null
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
                for (let uuid in this.emissions) {
                    const emission = this.emissions[uuid];
                    // const timeStart = dayjs(emission.timeStart);
                    const timeStart = emission.timeStartObj;
                    const timeDiff = timeStart.diff(this.dayStart.timeStart, 'second');

                    // console.table({
                    //     name: emission.name,
                    //     timeStart: emission.timeStart,
                    //     parsedTimeStart: timeStart.format('YYYY-MM-DD HH:mm:ss'),
                    //     schedulerTimeStart: this.dayStart.timeStart.format('YYYY-MM-DD HH:mm:ss'),
                    //     timeDiff: timeDiff
                    // });

                    // exclude items out of displayed range
                    if (timeDiff < 0 || timeDiff >= (60 * 60 * 24 * this.days.length)) {
                        continue;
                    }

                    const position = this.timeDiffToPosition(timeDiff);
                    emissions.push({
                        obj: emission,
                        timeDiff: timeDiff,
                        name: emission.name,
                        highlighted: emission.co.uuid === this.highlightedObjUuid,
                        dragged: emission.uuid === this.draggedEmissionUuid,
                        style: {
                            left: position.x + 'px',
                            top: position.y + 'px',
                            height: emission.duration / 60 / 60 / 1000 * this.pixelHeightPerHour + 'px',
                            width: this.pixelWidthPerDay + 'px'
                        }
                    })

                }
                return emissions;
            },
            // currentTimePosition(timeDiff) {
            //     const dayOffset = Math.floor(timeDiff / SECONDS_PER_DAY);
            //     const secondsOffset = timeDiff - (dayOffset * SECONDS_PER_DAY);
            //     return {
            //         x: this.pixelWidthPerDay * dayOffset,
            //         y: this.pixelHeightPerHour * secondsOffset / 60 / 60
            //     };
            // },
        },
        methods: {

            // hover / highlight handling
            highlightEmission: function (uuid, minCount=2) {
                if(this.readOnly) {
                    return;
                }
                // check if object in emissions
                // to prevent unnecessary updates
                let count = 0;
                for (const k in this.emissions) {
                    if(this.emissions[k].co.uuid === uuid) {
                        count++;
                    }
                }
                if(count >= minCount) {
                    this.highlightedObjUuid = uuid;
                }
            },
            unhighlightEmission: function () {
                if(this.highlightedObjUuid) {
                    this.highlightedObjUuid = null;
                }
            },

            // error handling
            addError: function(error) {
                console.warn('error', error.message, error.response);

                let errorMessage = {
                    uuid: uuid(),
                    messages: error.response.data || [error.message],
                };

                this.errors.unshift(errorMessage);
            },
            resetErrors: function() {
                this.errors = [];
            },

            // time- and offset calculations
            timeDiffToPosition: function (timeDiff) {
                const dayOffset = Math.floor(timeDiff / SECONDS_PER_DAY);
                const secondsOffset = timeDiff - (dayOffset * SECONDS_PER_DAY);
                return {
                    x: this.pixelWidthPerDay * dayOffset,
                    y: this.pixelHeightPerHour * secondsOffset / 60 / 60
                };
            },
            positionToTimeDiff: function(position) {
                const dayOffset = position.x / this.pixelWidthPerDay;
                return (dayOffset * SECONDS_PER_DAY * 1000) + (position.y / this.pixelHeightPerHour) * 60 * 60 * 1000;
            },

            // drag event calculate positions
            eventToXY: function({e, quantize = true, skipUnchanged = true}) {

                // check for changed position
                const rawPosition = this.rawDragEventPosition;
                if(skipUnchanged && rawPosition.x === e.clientX && rawPosition.y === e.clientY ) {
                    return null;
                    // return this.relativeDragEventPosition;
                } else {
                    rawPosition.x = e.clientX;
                    rawPosition.y = e.clientY;
                }

                // TODO: not s nice to always have to get the container/dimensions from DOM.
                // however, performance impact is close to zero...
                const container = this.$refs['calendar'];
                const node = container.getElementsByClassName("emissions")[0];
                const rect = node.getBoundingClientRect();

                // calculate positions relative to container
                let x = e.clientX - rect.left;
                let y = e.clientY - rect.top;

                if(quantize) {
                    x = quantizeNumber(x, this.pixelWidthPerDay);
                    y = quantizeNumber(y, this.pixelHeightPerHour / (60 / this.settings.snapMinutes));
                }

                // console.debug('eventToXZ', 'r', x, y);

                const relativeePosition = {
                    x: x,
                    y: y,
                };

                this.relativeDragEventPosition = relativeePosition;

                return relativeePosition;


            },

            // drop events

            /**
             *
             */
            dragenter: function (transferData, e) {
                if (DEBUG) console.debug('dragenter', transferData, e);
                if(transferData.ct === 'abcast.emission') {
                    this.draggedEmissionUuid = transferData.uuid;
                }
                this.hasDragging = true;
                this.emissionPlaceholder.transferData = transferData;
                this.emissionPlaceholder.visible = true;
            },
            dragleave: function (transferData, e) {
                if (DEBUG) console.debug('dragleave', transferData, e);
                if(transferData.ct === 'abcast.emission') {
                    return;
                }
                this.hasDragging = false;
                this.emissionPlaceholder.visible = false;
            },


            dragover: function (transferData, e) {

                const position = this.eventToXY({e});
                // if (DEBUG) console.debug('dragover', position);

                if(position) {

                    // TODO: should not be needed!
                    this.emissionPlaceholder.visible = true;
                    this.emissionPlaceholder.position = position;

                    // this.emissionPlaceholder.style = {
                    //     left: position.x + 'px',
                    //     top: position.y + 'px',
                    //     width: this.pixelWidthPerDay + 'px',
                    //     height: (transferData.duration / 60 / 60 / 1000 * this.pixelHeightPerHour) + 'px',
                    // };
                }

            },
            drop: function (transferData, e) {

                const position = this.eventToXY({e, skipUnchanged: false});
                const timeDiff = this.positionToTimeDiff(position);
                const timeStart = this.dayStart.timeStart.add(timeDiff, 'millisecond');
                const formattedTimeStart = timeStart.format('YYYY-MM-DD HH:mm');

                console.debug('drop', transferData,  position, timeDiff, formattedTimeStart, e);

                // check if we have to update an existing emission or if
                // it is a copy resp. new item

                if(! e.altKey && transferData.ct === 'abcast.emission') {
                    console.debug('reschedule emission');
                    // this.updateEmission(transferData, formattedTimeStart);
                    this.updateEmission(transferData, {'time_start': formattedTimeStart});
                } else if (transferData.ct === 'abcast.emission') {
                    console.debug('duplicated emission', transferData.co);
                    this.createEmission(transferData.co, formattedTimeStart);
                } else {
                    console.debug('added item to scheduler', transferData);
                    this.createEmission(transferData, formattedTimeStart);
                }


                // this.updateEmission(transferData, formattedTimeStart);

            },

            emissionDrag: throttle(function(transferData, e) {

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
            updateEmission: function(emission, payload) {
                // console.debug(emission);
                const dispatch = this.$store.dispatch('scheduler/updateEmission', {
                    emission: emission,
                    payload: payload
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
            createEmission: function(contentObj, timeStart) {
                console.debug('createEmission', contentObj);
                const dispatch = this.$store.dispatch('scheduler/createEmission', {
                    contentObj: contentObj,
                    timeStart: timeStart,
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
            showEmissionEditor: function(uuid) {
                if(this.readOnly) {
                    return;
                }
                this.emissionInEditorUuid = uuid;
            },
            closeEmissionEditor: function() {
                this.emissionInEditorUuid = null;
            },
        },
        watch: {
            highlightObjUuid: function (uuid) {
                if(uuid) {
                    this.highlightEmission(uuid, 1);
                } else {
                    this.unhighlightEmission();
                }
            }
        },
    }
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
                background: #ffffff;
            }
        }

        .current-time {
            position: absolute;
            width: 100%;
            &__line {
                //background: orangered;
                height: 0;
                border-bottom: 1px dotted rgba(255, 69, 0, .5);
            }
            &__time {
                position: absolute;
                color: orangered;
                // left: -45px;
                left: -60px;
                font-size: 11px;
                line-height: 11px;
                top: -5px;
            }
            &__marker {
                position: absolute;
                /*height: 10px;*/
                /*width: 10px;*/
                width: 0;
                height: 0;
                border-style: solid;
                top: 0;
                transform: translate(0, -4.5px);

                &--left {
                    left: -10px;
                    border-width: 5px 0 5px 8px;
                    border-color: transparent transparent transparent orangered;
                }
                &--right {
                    right: -10px;
                    border-width: 5px 8px 5px 0;
                    border-color: transparent orangered transparent transparent;
                }

            }
        }

        .errors-container {

            position: fixed;
            z-index: 1001;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(26, 5, 0, 0.66);

            .errors {
                background: orangered;
                color: white;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding: 20px;

                .error {
                    white-space: pre-line;
                    text-align: left;
                    font-size: 120%;
                    line-height: 180%;
                }
            }
        }

    }

    .fade-in-out-enter-active {
        transition: opacity 200ms;
    }

    .fade-in-out-leave-active {
        transition: opacity .800ms;
    }

    .fade-in-out-enter, .fade-in-out-leave-to {
        opacity: 0;
    }


    .emission-list-leave-active {
      /*filter: grayscale(100%);*/
      /*transition: opacity 2500ms;*/
    }
    .emission-list-enter-active {
      transition: opacity 200ms;
    }
    .emission-list-enter, .emission-list-leave-to {
      opacity: 0;
    }

</style>

<template>
    <div
        :style="{ height: calendarHeight + 50 + 'px' }"
        ref="calendar"
        class="calendar">

        <grid
            :pixel-height-per-hour="pixelHeightPerHour"
            :days="days"></grid>

        <drop
            @dragenter="dragenter"
            @dragleave="dragleave"
            @dragover="dragover"
            @drop="drop"
            class="emissions">

            <emission-placeholder
                :pixelWidthPerDay="pixelWidthPerDay"
                :pixelHeightPerHour="pixelHeightPerHour"
                :placeholder="emissionPlaceholder"
                ></emission-placeholder>

            <transition-group name="emission-list" tag="div">
                <drag
                    v-for="emission in mappedEmissions"
                    class="emission-container"
                    @drag="emissionDrag"
                    :draggable="(! readOnly && ! emission.obj.hasLock)"
                    :key="emission.obj.uuid"
                    :transfer-data="emission.obj"
                    :style="emission.style">

                    <template slot="image">
                        <div><!-- empty drag handler --></div>
                    </template>

                    <emission
                        :emission="emission"
                        @dblclick="showEmissionEditor"
                        @mouseover="highlightEmission"
                        @mouseleave="unhighlightEmission"
                    ></emission>
                </drag>
            </transition-group>

        </drop>

        <div
            v-if="currentTime"
            :style="{ top: currentTimeY + 'px'}"
            class="current-time">
            <div
                class="current-time__time">
                {{ currentTime.format('H:mm:s') }}
            </div>
            <div
                class="current-time__marker current-time__marker--left"></div>
            <div
                class="current-time__marker current-time__marker--right"></div>
            <div
                class="current-time__line"></div>
        </div>

        <transition
            name="fade-in-out">
            <div
                v-if="(errors && errors.length)"
                @click="resetErrors"
                class="errors-container">
                <div
                    v-for="error in errors"
                    class="errors"
                    :key="error.uuid">
                    <p
                        v-for="(message, index) in error.messages"
                        class="error"
                        :key="`error-message-${index}`">{{ message }}</p>
                </div>

            </div>
        </transition>

        <emission-editor
            @close="closeEmissionEditor"
            :uuid="emissionInEditorUuid"></emission-editor>

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
