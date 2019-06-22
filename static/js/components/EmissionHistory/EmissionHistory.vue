<script>

    const DEBUG = false;
    const NEARBY_HOURS = 48;

    import ClickOutside from 'vue-click-outside';
    import dayjs from 'dayjs';
    import toObject from 'dayjs/plugin/toObject';
    import relativeTime from 'dayjs/plugin/relativeTime';

    import EmissionHistoryMatrix from './EmissionHistoryMatrix.vue';

    dayjs.extend(toObject);
    dayjs.extend(relativeTime);

    export default {
        name: 'EmissionHistory',
        components: {
            'matrix': EmissionHistoryMatrix,
        },
        directives: {
            ClickOutside,
        },
        props: {
            objCt: String,
            objUuid: String,
            hasWarning: Boolean
        },
        data() {
            return {
                nearbyEmissionsVisible: false,
                matrixVisible: false,
            }
        },
        mounted: function () {

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
                if(! this.lastEmission) {
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
                if(! this.nextEmission) {
                    return null;
                }
                const now = dayjs(new Date());
                const time = dayjs(this.nextEmission.timeStart);
                return Math.abs(time.diff(now, 'hour')) < NEARBY_HOURS;
            }
        },
        methods: {
            loadHistory: function (e) {
                this.$store.dispatch('objectHistory/loadObjectHistory', {objCt: this.objCt, objUuid: this.objUuid});
            },
            showNearbyEmissions: function (e) {
                if (!this.emissionHistory) {
                    this.loadHistory();
                    console.log('history not loaded - trigger!');
                }
                this.nearbyEmissionsVisible = true;
            },
            hideNearbyEmissions: function (e) {
                this.nearbyEmissionsVisible = false;
            },
            toggleMatrix: function(e) {
                if(! this.matrixVisible) {
                    this.showMatrix();
                } else {
                    this.hideMatrix();
                }
            },
            showMatrix: function() {
                this.matrixVisible = true;
            },
            hideMatrix: function() {
                this.matrixVisible = false;
            },
        },
        filters: {
            // dateTime: function (value) {
            //     if (!value) return '';
            //     console.debug(value, dayjs(value).format('DD/MM/YYYY'));
            //     return dayjs(value).format('DD/MM/YYYY');
            // },
            relativeDateTime: function (value) {
                if (!value) return '';
                return dayjs(value).fromNow();
            },
        }
    }
</script>
<style lang="scss" scoped>
    .emission-history {
        $self: &;
        position: relative;

        &__indicator {
            background: white;
            height: 21px;
            width: 21px;
            display: inline-flex;
            justify-content: center;
            position: absolute;
            right: 0;
            font-weight: 400;
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
            background: white;
            right: 0;
            top: 21px;
            width: 197px;

            > div {
                padding: 2px 6px;
                border-left: 4px solid limegreen;
                background: rgba(50, 205, 50, 0.15);
                margin: 1px 0;
                &.has-warning {
                    // background: red;
                    border-left: 4px solid orangered;
                    color: orangered;
                    background: rgba(255, 69, 0, 0.15);
                    font-weight: 400;
                }
            }

        }

        &__matrix-container {
            position: absolute;
            border: 1px solid #000;
            top: 21px;
            min-width: 640px;
            z-index: 999;
            transform: translateX(-50%);
            background: white;
        }
    }
</style>

<template>
    <div
        v-click-outside="hideMatrix"
        :class="{ 'emission-history--has-warning': hasWarning }"
        class="emission-history">
        <div
            @mouseover="showNearbyEmissions"
            @mouseleave="hideNearbyEmissions"
            @click="toggleMatrix"
            class="emission-history__indicator">
            <span>H</span>
        </div>
        <div
            v-if="nearbyEmissionsVisible"
            class="emission-history__nearby-emissions">
            <div
                :class="{ 'has-warning': lastEmissionWarning }"
                >
                <span>Last emission</span>
                <ul>
                    <li
                        v-if="lastEmission">
                        {{ lastEmission.timeStart | relativeDateTime }}
                    </li>
                    <li
                        v-else>
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
                        v-if="nextEmission">
                        {{ nextEmission.timeStart | relativeDateTime }}
                    </li>
                    <li
                        v-else>
                        No emission schduled
                    </li>
                </ul>
            </div>
        </div>
        <div
            class="emission-history__matrix-container"
            v-if="matrixVisible">
                <matrix
                    :emission-history="emissionHistory"
                ></matrix>
        </div>
    </div>
</template>
