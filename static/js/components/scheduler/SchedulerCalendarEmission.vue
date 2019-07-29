<script>

    const DEBUG = false;
    import {backgroundColors} from './constants';
    import {hexToRGBA} from './utils';

    export default {
        name: 'SchedulerCalendarEmission',
        props: {
            emission: Object,
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
                    // backgroundColor: hexToRGBA(color, .8),
                    borderColor: hexToRGBA(color, 1),
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
            background: rgba(255, 255, 255, 0.80);
            height: calc(100% - 1px);
            cursor: pointer;
            transition: background 200ms;
            position: relative;
            display: flex;
            flex-direction: column;
            border-left: 2px solid #fff;

            &:hover {
                background: rgba(126, 235, 157, 0.85);
            }

            &__title {
                background: rgba(0, 0, 0, .025);
                padding: 0 4px;
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
            }

            &:hover & {
                &__title {
                    overflow: visible;
                    white-space: normal;
                    z-index: 999;
                }
            }

            &.is-highlighted {
                background: rgba(235, 193, 64, 0.85) !important;
            }

            &.is-dragged {
                opacity: .2;
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
                <!--
                <br>
                <small>{{ emission.obj.name }}</small>
                -->
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
        </div>

    </div>
</template>
