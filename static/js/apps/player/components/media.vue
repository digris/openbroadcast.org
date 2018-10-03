<script>
    import debounce from 'debounce';
    import Waveform from './waveform.vue';

    const DEBUG = true;

    export default {
        props: [
            'item'
        ],
        components: {
            Waveform
        },
        data() {
            return {
                seek_active: false,
                seek_position: null
            }
        },
        mounted: function () {
            if (DEBUG) console.debug('Waveform - mounted');
        },
        computed: {
            position: function () {
                return (this.item.playhead_position > 0.3) ? this.item.playhead_position - 0.3 : 0;
            },
        },
        methods: {
            seek: function (item, e) {
                const x = e.clientX;
                //const w = e.target.getBoundingClientRect().width;
                const w = window.innerWidth;
                const p = Math.round((x / w) * 100);

                console.debug('$emit', 'seek', p, item)

                this.$emit('seek', item, p);
            },
            seek_move: function(e) {
                // console.debug('seek_move', e);
                this.seek_position = Math.round(e.clientX / window.innerWidth * 100);
            },
            seek_enter: function(e) {
                //console.log('seek_enter > add listener', e);
                document.removeEventListener('mousemove', this.seek_move);
                document.addEventListener('mousemove', this.seek_move);
            },
            seek_leave: function(e) {
                // console.log('seek_leave > remove listener', e);
                document.removeEventListener('mousemove', this.seek_move);
            },


            // seek_enter: debounce(function (item, e) {
            //     console.log('seek_enter > add listener', e);
            //     document.removeEventListener('mousemove', this.seek_move);
            //     document.addEventListener('mousemove', this.seek_move);
            // }, 100),
            // seek_leave: debounce(function (item, e) {
            //     console.log('seek_leave > remove listener', e);
            //     document.removeEventListener('mousemove', this.seek_move);
            //     this.seek_position = null;
            // }, 50),
        },
        filters: {
            sec_to_time: function (value) {
                return ms_to_time(value * 1000)
            },
            ms_to_time: function (value) {
                return ms_to_time(value)
            }
        },
    }

    const ms_to_time = function (time) {

        if (time == undefined) {
            return '';
        }

        if (time == 0) {
            return '00:00';
        }

        time = Math.abs(time);

        let millis = time % 1000;
        time = parseInt(time / 1000);
        let seconds = time % 60;
        time = parseInt(time / 60);
        let minutes = time % 60;
        time = parseInt(time / 60);
        let hours = time % 24;
        let out = "";

        if (hours && hours > 0) {
            if (hours < 10) {
                out += '0';
            }
            out += hours + ':';
        } else {
            // out += '0' + ':';
        }

        if (minutes && minutes > 0) {
            if (minutes < 10) {
                out += '0';
            }
            out += minutes + ':';
        } else {
            out += '00' + ':';
        }

        if (seconds && seconds > 0) {
            if (seconds < 10) {
                out += '0';
            }
            out += seconds + '';
        } else {
            out += '00' + '';
        }

        return out.trim();
    };

</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .item {
        color: #5a5a5a;
        background: #fafafa;
        border-bottom: 1px solid #eaeaea;
        // margin-bottom: 4px;
        &.is-playing {
            background: $primary-color-a-bg-light;
        }
        .primary-content {
            padding: 2px 4px;
            display: flex;
            .meta {
                padding-left: 10px;
                flex-grow: 1;
            }
            .time {
                padding-right: 10px;
                small {
                    opacity: 0.5;
                }
            }
        }
        .playhead {
            cursor: crosshair;
            height: 10px;
            position: relative;
            .progress-container {
                position: absolute;
                width: 100%;
                z-index: 9;
                background: white;
                height: 2px;
                top: 5px;
                .progress-indicator {
                    height: 2px;
                    top: 0;
                    left: 0;
                    width: 25%;
                    position: absolute;
                    background: $primary-color-a;
                }
            }
            .seek-container {
                background: rgba(255, 165, 0, 0.05);
                border-right: 1px solid $primary-color-b;
                position: absolute;
                top: 0;
                height: 12px;
                width: 50%;
                z-index: 10;
                display: none;
            }
            &:hover {
                .seek-container {
                    display: block;
                }
            }
        }
    }

</style>

<template>
    <div :key="item.key" class="item" v-bind:class="{ 'is-playing': item.is_playing }">
        <div class="primary-content">
            <div class="controls">
                <span v-if="(! item.is_playing)" @click="$emit('play', item)">
                    <i class="fa fa-play"></i>
                </span>
                <span v-else @click="$emit('pause', item)">
                    <i class="fa fa-stop"></i>
                </span>
            </div>

            <div class="meta">
                <!--<span>Playing: {{ item.is_playing }}{{ item.playhead_position }}</span><br>-->
                <span>{{ item.content.name }}</span>
                <br>
                <a href="#">{{ item.content.artist_display }}</a>
                |
                <a href="#">{{ item.content.release_display }}</a>

            </div>

            <div class="time">
                <small v-if="item.is_playing">{{ item.playhead_position_ms | ms_to_time }}</small>
                {{ item.duration | ms_to_time }}
                <br>
                <small v-if="item.is_buffering">buffering</small>
                <!--
                {{ item.from | ms_to_time }} - {{ item.to | ms_to_time }}
                -->
                <!--<br>
                {{ item.fade_to }} - {{ item.fade_from }}-->
                <br>
            </div>

            <div class="actions">
                (( actions ))
            </div>
        </div>


        <div v-if="item.errors">
            <div v-for="error in item.errors">
                {{ error }}
            </div>
        </div>

        <!--
        v-on:mouseover="seek_enter(item, $event)"  v-on:mouseleave="seek_leave(item, $event)"
        -->

        <div v-if="item.is_playing" class="playhead" @click="seek(item, $event)" v-on:mouseover="seek_enter(item, $event)"  v-on:mouseleave="seek_leave(item, $event)">

            <!--<svg width="100%" height="8px" viewBox="0 0 100 8" preserveAspectRatio="none" @mouseover="seek_enter(item, $event)" @mouseout="seek_leave(item, $event)">-->
            <!---->

            <div class="svg-container">
                <!--<svg width="100%" height="8px" viewBox="0 0 100 8" preserveAspectRatio="none">

                    <rect width="100%" height="8" style="fill:rgba(0,255,255,0.5)"></rect>

                    <rect width="100" height="2" style="fill:rgba(100,200,0,0.8)"></rect>
                    <rect :width="position" height="2" style="fill:rgba(100,100,100,0.8)"></rect>


                    <rect v-if="seek_position" :width="seek_position" height="8" style="fill:rgba(255,0,255,0.5)"></rect>

                </svg>-->
            </div>

            <div class="progress-container">
                <div class="progress-indicator" v-bind:style="{ width: position + '%' }">

                </div>
            </div>


            <div class="seek-container" v-bind:style="{ width: seek_position + '%' }">

            </div>


        </div>
    </div>
</template>
