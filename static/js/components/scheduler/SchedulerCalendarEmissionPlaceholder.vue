<script>

    const DEBUG = true;

    export default {
        name: 'SchedulerCalendarEmissionPlaceholder',
        props: {
            placeholder: Object,
            pixelWidthPerDay: Number,
            pixelHeightPerHour: Number,
        },
        data() {
            return {
                detailsVisible: false,
            }
        },
        methods: {},
        computed: {
            visible() {
                return this.placeholder.visible
            },
            width() {
                return this.pixelWidthPerDay;
            },
            height() {
                if(! this.placeholder.transferData) {
                    return 0;
                }
                return Math.round(this.placeholder.transferData.duration / 60 / 60 / 1000 * this.pixelHeightPerHour);
            },
            position() {
                return this.placeholder.position;
            },
            style() {
                return {
                    width: `${this.width}px`,
                    height: `${this.height}px`,
                    left: `${this.position.x}px`,
                    top: `${this.position.y}px`,
                }
            },
        }
    }
</script>
<style lang="scss" scoped>
    .emission-placeholder {
        // background: yellow;
        position: absolute;
        z-index: 999;
        pointer-events: none;

        margin: 1px 0 1px 1px;
        background: rgba(255, 255, 0, 0.85);
        height: calc(100% - 1px);
        font-size: 80%;

        transition: none;

        &__title {
            background: rgba(0, 0, 0, 0.025);
            padding: 0 4px;
        }
    }

    .fade-in-out-enter-active {
        transition: opacity 100ms;
    }

    .fade-in-out-leave-active {
        transition: opacity .800ms;
    }

    .fade-in-out-enter, .fade-in-out-leave-to {
        opacity: 0;
    }
</style>

<template>
    <transition
        name="fade-in-out">
        <div
            v-if="visible"
            class="emission-placeholder"
            :style="style">
            <div
                v-if="placeholder.transferData"
                class="emission-placeholder__title">
                <span v-if="placeholder.transferData.series">
                    {{ placeholder.transferData.series }}
                </span>
                <span v-else>
                    {{ placeholder.transferData.name }}
                </span>
            </div>
        </div>
    </transition>
</template>
