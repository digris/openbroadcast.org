<script>

    const DEBUG = false;
    import {backgroundColors} from './constants';
    import ColorChooser from '../../components/ui/ColorChooser.vue';

    export default {
        name: 'SchedulerCalendarNavigation',

        props: {
            settings: Object,
        },
        components: {
            'color-chooser': ColorChooser,
        },
        data() {
            return {
                emissionColors: backgroundColors,
            }
        },
        methods: {

        },
        computed: {
            numDays() {
                if(this.settings && this.settings.numDays) {
                    return this.settings.numDays;
                }
                return null;
            },
            snapMinutes() {
                if(this.settings && this.settings.snapMinutes) {
                    return this.settings.snapMinutes;
                }
                return null;
            },
            emissionColor() {
                if(this.settings && this.settings.emissionColor != undefined) {
                    return this.settings.emissionColor;
                }
                return null;
            }
        }
    }
</script>
<style lang="scss" scoped>
    .calendar-navigation {
        display: flex;

        .action {
            cursor: pointer;
            background: white;
            padding: 1px 8px;
            display: inline-flex;
            border: 1px solid #dadada;
            &:hover {
                background: #6633CC;
                border-color: #6633CC;
                border-radius: 2px;
                color: white;
            }
            &.is-current {
                border-color: #6633CC;
            }
        }

        &__center {
            flex-grow: 1;
            display: flex;
            justify-content: center;
            .action {
                margin-left: 2px;
                margin-right: 2px;
            }
        }

        &__left {
            .action {
                margin-right: 4px;
            }
        }

        &__right {
            .action {
                margin-left: 4px;
            }
        }

    }
</style>

<template>
    <div class="calendar-navigation">

        <div class="calendar-navigation__left">
            <span
                class="action"
                @click.prevent="$emit('updateDaysOffset', 7)">
                &#x3C; Week
            </span>
            <span
                class="action"
                @click.prevent="$emit('updateDaysOffset', 1)">
                &#x3C; Day
            </span>
        </div>

        <div class="calendar-navigation__center">
            <span
                class="action"
                @click.prevent="$emit('decreaseVerticalSize')">
                -
            </span>
            <span
                class="action"
                @click.prevent="$emit('increaseVerticalSize')">
                +
            </span>
            <span
                :class="{ 'is-current': numDays === 7 }"
                class="action"
                @click.prevent="$emit('setNumDays', 7)">
                7 Days
            </span>
            <span
                :class="{ 'is-current': numDays === 14 }"
                class="action"
                @click.prevent="$emit('setNumDays', 14)">
                14 Days
            </span>
            <span
                :class="{ 'is-current': numDays === 28 }"
                class="action"
                @click.prevent="$emit('setNumDays', 28)">
                28 Days
            </span>
            <span
                class="action"
                @click.prevent="$emit('reset')">
                Reset
            </span>
            <span
                :class="{ 'is-current': snapMinutes === 5 }"
                class="action"
                @click.prevent="$emit('setSnapMinutes', 5)">
                5
            </span>
            <span
                :class="{ 'is-current': snapMinutes === 15 }"
                class="action"
                @click.prevent="$emit('setSnapMinutes', 15)">
                15
            </span>
            <span
                :class="{ 'is-current': snapMinutes === 30 }"
                class="action"
                @click.prevent="$emit('setSnapMinutes', 30)">
                30
            </span>
            <color-chooser
                @select="$emit('setColor', $event)"
                :width="(48)"
                :height="(22)"
                :colors="emissionColors"
                :selected-color="emissionColor">
            </color-chooser>

        </div>

        <div class="calendar-navigation__right">
            <span
                class="action"
                @click.prevent="$emit('updateDaysOffset', -1)">
                Day &#x3E;
            </span>
            <span
                class="action"
                @click.prevent="$emit('updateDaysOffset', -7)">
                Week &#x3E;
            </span>
        </div>

    </div>
</template>
