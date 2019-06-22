<script>

    const DEBUG = true;

    import dayjs from 'dayjs';
    import advancedFormat from 'dayjs/plugin/advancedFormat';
    dayjs.extend(advancedFormat);
    import {backgroundColors} from './constants';
    import {hexToRGBA} from './utils';
    import SchedulerCalendarEmissionContent from './SchedulerCalendarEmissionContent.vue';
    import Modal from '../../components/ui/Modal.vue';
    import UserInline from '../../components/ui/UserInline.vue';
    import EmissionHistoryMatrix from '../EmissionHistory/EmissionHistoryMatrix.vue';

    export default {
        name: 'SchedulerCalendarEmissionEditor',
        props: {
            uuid: String,
        },
        components: {
            'modal': Modal,
            'user-inline': UserInline,
            'matrix': EmissionHistoryMatrix,
            'content-obj': SchedulerCalendarEmissionContent,
        },
        data() {
            return {
                // visible: true,
                backgroundColors: backgroundColors,
            }
        },
        methods: {
            close: function () {
                this.$emit('close');
            },
            loadEmissionDetails: function() {
                if(this.uuid) {
                    const dispatch = this.$store.dispatch('scheduler/loadEmission', this.uuid);
                }
            },
            setColor: function(color) {
                this.updateEmission({
                   color: color,
                });
            },
            updateEmission: function(payload) {
                const dispatch = this.$store.dispatch('scheduler/updateEmission', {emission: this.emission, payload: payload});
            },
            deleteEmission: function() {
                const dispatch = this.$store.dispatch('scheduler/deleteEmission', this.uuid);
                dispatch.then((response) => {
                    this.$emit('close');
                }, (error) => {
                    console.warn('error', error.message, error.response);
                });

            },
            // history
            loadEmissionHistory: function () {
                if(!this.contentObj) {
                    return;
                }
                this.$store.dispatch('objectHistory/loadObjectHistory', {objCt: this.contentObj.ct, objUuid: this.contentObj.uuid});
            },
        },
        computed: {
            visible() {
                return this.uuid != null;
            },
            emission() {
                if(!this.uuid) {
                    return null;
                }
                return this.$store.getters['scheduler/emissionByUuid'](this.uuid);
            },
            contentObj() {
                if(!this.emission) {
                    return null;
                }
                return this.emission.co;
            },
            contentObjStyle() {
                if(!this.contentObj) {
                    return null;
                }
                const color = backgroundColors[this.emission.color];
                return {
                    backgroundColor: hexToRGBA(color, .2),
                    //backgroundColor: `rgba(${color}, .2)`,
                }

            },
            emissionHistory() {
                if(!this.contentObj) {
                    return null;
                }
                console.debug('history', this.contentObj.ct, this.contentObj.uuid);
                return this.$store.getters['objectHistory/objectHistoryByKey'](this.contentObj.ct, this.contentObj.uuid);
            },
            formattedTimes() {
                if(!this.emission) {
                    return null;
                }
                const start = dayjs(this.emission.timeStart);
                const end = dayjs(this.emission.timeEnd);
                return {
                    date: start.format('ddd. D MMMM YYYY'),
                    start: start.format('H:mm'),
                    end: end.format('H:mm'),
                }
            }
        },
        watch: {
            uuid: function (oldUuid, newUuid) {
                this.loadEmissionDetails();
                this.loadEmissionHistory();
            }
        },
    }
</script>
<style lang="scss" scoped>
    .emission-editor {
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;

        .content-object {
            margin: 20px 0;
        }

        &__scheduling {
            text-align: center;
            .scheduling-timing {
                font-size: 150%;
                line-height: 160%;
            }
        }

        &__history {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        &__actions {
            display: flex;
            flex-direction: column;
            .background-colors {
                display: flex;
                width: 100%;
                .color {
                    flex-grow: 1;
                    padding: 8px;
                    cursor: pointer;
                }
            }

            .delete {
                margin-top: 16px;
                &__confirm {
                    text-align: center;
                    border: 2px solid #6633CC;
                    background: #fff;
                    color: #6633CC;
                    font-size: 120%;
                    padding: 6px;
                    cursor: pointer;

                    &:hover {
                        color: #fff;
                        background: #6633CC;
                        border-radius: 4px;
                    }
                }
            }

        }

    }
</style>

<template>
    <modal
        :show="visible"
        @close="close">
        <div slot="content" class="emission-editor">
            <content-obj
                v-if="contentObj"
                :style="contentObjStyle"
                :content-obj="contentObj"
            ></content-obj>
            <div
                class="emission-editor__scheduling">
               <div
                   v-if="formattedTimes"
                   class="scheduling-timing">
                   <span>{{ formattedTimes.date }}</span>
                   <br>
                   <span>{{ formattedTimes.start }}</span>
                   &mdash;
                   <span>{{ formattedTimes.end }}</span>
               </div>
               <div
                   v-if="(emission && emission.user)"
                   class="scheduling-programmer">
                    by:
                    <user-inline
                        v-if="emission.user"
                        :user="emission.user"></user-inline>
               </div>
            </div>
            <div
                class="emission-editor__history">
                <matrix
                    v-if="emissionHistory"
                    :emission-history="emissionHistory"
                ></matrix>
            </div>
            <div
                class="emission-editor__actions">
                <div
                    class="background-colors">
                    <div
                        v-for="(color, index) in backgroundColors"
                        :key="(`${color}`)"
                        :style="{'background-color': color}"
                        @click="setColor(index)"
                        class="color">
                        <span>{{ color }}{{ index }}</span>
                    </div>
                </div>
                <div
                    v-if="(contentObj && !emission.hasLock)"
                    class="delete">
                    <div
                        @click="deleteEmission"
                        class="delete__confirm">
                        <span>Remove emission</span>
                    </div>
                </div>
            </div>
        </div>
    </modal>
</template>
