<script>

    const DEBUG = false;
    import {backgroundColors} from './constants';
    import {hexToRGBA} from './utils';
    import SchedulerCalendarEmissionContent from './SchedulerCalendarEmissionContent.vue';

    export default {
        name: 'SchedulerCalendarEmission',
        props: {
            emission: Object,
        },
        components: {
            // 'content-obj': SchedulerCalendarEmissionContent,
        },
        data() {
            return {
                detailsVisible: false,
            }
        },
        methods: {
            dblclick: function () {
                this.$emit('dblclick', this.emission.obj.uuid);
            },
            onMouseOver: function () {
                this.$emit('mouseover', this.emission.obj.co.uuid);
                this.detailsVisible = true;
            },
            onMouseLeave: function () {
                this.$emit('mouseleave');
                this.detailsVisible = false;
            },

        },
        computed: {
            style() {
                const color = backgroundColors[this.emission.obj.color];
                return {
                    backgroundColor: hexToRGBA(color, .8),
                }
            },
        }
    }
</script>
<style lang="scss" scoped>

        // background: red;
        .emission {
            // border: 1px solid rgba(0, 0, 0, 0.25);
            margin: 1px 0 1px 1px;
            background: rgba(132, 255, 166, 0.85);
            height: calc(100% - 1px);
            cursor: pointer;
            font-size: 80%;
            transition: background 200ms;
            position: relative;

            display: flex;
            flex-direction: column;

            &__title {
                background: rgba(0, 0, 0, 0.025);
                padding: 0 4px;
            }

            &:hover {
                background: rgba(126, 235, 157, 0.85);
            }

            &.is-highlighted {
                background: rgba(235, 88, 0, 0.85) !important;
            }

            &.is-dragged {
                opacity: .2;
            }

            &__visual {
                height: auto;
                overflow: hidden;
                img {
                    filter: grayscale(1);
                    opacity: .2;
                    max-height: 100%;
                    width: 100%;
                    object-fit: cover;
                    object-position: center;
                }
            }

            // detail block, visible on hover
            &__details {
                background: #000;
                position: absolute;
                top: 0;
                left: calc(100% + 4px);
                color: white;
                min-width: 140px;
            }
        }
</style>

<template>
    <div
        @dblclick="dblclick"
        @mouseover="onMouseOver"
        @mouseleave="onMouseLeave"
        :style="style"
        :class="{ 'is-highlighted': emission.highlighted, 'is-dragged': emission.dragged }"
        class="emission">
        <div
            class="emission__title">
            <span v-if="emission.obj.series">
                {{ emission.obj.series }}
            </span>
            <span v-else>
                {{ emission.obj.name }}
            </span>
        </div>
        <!--
        <div
            v-if="emission.obj.image"
            class="emission__visual">
            <img :src="emission.obj.image">
        </div>
        -->
        <div v-if="detailsVisible"
            class="emission__details">

            {{ emission.obj.co.name }}

            <!--
            <content-obj
                size="small"
                :content-obj="emission.obj.co"></content-obj>
            -->
        </div>

    </div>
</template>
