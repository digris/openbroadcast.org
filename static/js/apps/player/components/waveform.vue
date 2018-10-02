<script>
    export default {
        props: [
            'item'
        ],
        data() {
            return {
                greeting: 'Hello',
            }
        },
        computed: {
            position: function () {
                return this.item.playhead_position - 0.3;
            },
            cue_fade_points: function () {
                let item = this.item;

                let x1 = Math.floor(item.from / item.duration * 100);
                let x2 = Math.floor(item.fade_to / item.duration * 100);
                let x3 = Math.floor(item.fade_from / item.duration * 100);
                let x4 = Math.floor(item.to / item.duration * 100);

                return `${x1},20 ${x2},0 ${x3},0 ${x4},20`
            },
            mask_left: function () {
                let item = this.item;

                let x1 = Math.floor(item.from / item.duration * 100);
                let x2 = Math.floor(item.fade_to / item.duration * 100);
                return `0,0 ${x2},0 ${x1},20 0,20`
            },
            mask_right: function () {
                let item = this.item;

                let x3 = Math.floor(item.fade_from / item.duration * 100);
                let x4 = Math.floor(item.to / item.duration * 100);
                return `${x3},0 100,0 100,20 ${x4},20`
            },
            mask_style: function () {
                if (this.item.is_playing) {
                    //return 'fill:rgba(188,245,224,0.7);';
                    return 'fill:rgba(255,255,255,0.7);';
                } else {
                    return 'fill:rgba(255,255,255,0.9);';
                }
            }
        },
        methods: {
            seek: function (e) {
                const x = e.clientX;
                //const w = e.target.getBoundingClientRect().width;
                const w = window.innerWidth;
                const p = Math.round((x / w) * 1000) / 10;

                console.debug('waveform - $emit', 'seek', p);

                this.$emit('seek', this.item, p);
            },
        },

    }

</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .waveform {
        cursor: crosshair;
        position: relative;
        height: 20px;
        .waveform-rubberband {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 20px;
        }
        .waveform-image {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 20px;
            img {
                width: 100%;
                height: 20px;
            }
        }
    }
</style>

<template>
    <div @click="seek($event)" class="waveform">
        <div class="waveform-rubberband">
            <svg width="100%" height="20px" viewBox="0 0 100 20" preserveAspectRatio="none">
                <rect :width="position" height="20" style="fill:rgba(100,100,100,0.8)"></rect>
                <polygon
                    :points="cue_fade_points"
                    style="fill:rgba(0,0,0,0.25);">>
                </polygon>

                <polygon
                    :points="mask_left"
                    :style="mask_style"></polygon>

                <polygon
                    :points="mask_right"
                    :style="mask_style"></polygon>
            </svg>
        </div>

        <div v-if="(item.content && item.content.assets.waveform)" class="waveform-image">
            <img v-bind:src="item.content.assets.waveform"/>
        </div>
    </div>
</template>
