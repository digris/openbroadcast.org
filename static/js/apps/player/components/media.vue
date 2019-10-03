<script>
    import {templateFilters} from '../../../utils/template-filters';
    const DEBUG = false;

    export default {
        props: [
            'item'
        ],
        components: {

        },
        data() {
            return {
                seek_active: false,
                seek_position: null,
                is_hover: false
            }
        },
        mounted: function () {
            if (DEBUG) console.debug('media - mounted');
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
            remove: function (item, e) {
                this.$emit('remove', item);
            },
            collect: function(item, e) {
                const _e = new CustomEvent('collector:collect', {detail: [item] });
                window.dispatchEvent(_e);
            }
        },
        filters: templateFilters,
    }

</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';

    .item {
        position: relative;
        color: #5a5a5a;
        background: #fafafa;
        border-bottom: 1px solid #eaeaea;
        &.is-playing {
            background: $primary-color-a-bg-light;
        }
        &.has-errors {
            cursor: not-allowed;
            background: #fffdea;
            .primary-content {
                opacity: 0.5;
                filter: grayscale(100);
            }
        }
        .primary-content {
            padding: 2px 4px;
            display: flex;
            .controls {
                display: flex;
                align-items: center;
                justify-content: center;
                span {
                    width: 20px;
                    height: 20px;
                    padding-top: 2px;
                    text-align: center;
                    display: block;
                    cursor: pointer;
                    opacity: 0.75;
                }
            }
            .meta {
                padding-left: 10px;
                flex-grow: 1;
            }
            .time {
                padding-right: 10px;
                padding-top: 8px;
                font-size: 90%;
                small {
                    opacity: 0.5;
                }
            }
            .actions {
                display: flex;
                align-items: center;
                justify-content: center;
                span {
                    width: 20px;
                    height: 20px;
                    padding-top: 2px;
                    text-align: center;
                    display: block;
                    cursor: pointer;
                    opacity: 0.75;
                }
            }


            .__expandable-actions {
                position: absolute;
                background: red;
                height: 100%;
                top: 0;
                right: 0;
                z-index: 20;
                width: 20px;
            }

        }
        .errors {
            padding: 0 0 2px 34px;
            color: #d47327;
            font-size: 90%;
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
    <div :key="item.key" class="item" @mouseover="is_hover=true" @mouseleave="is_hover=false" v-bind:class="{ 'is-playing': item.is_playing, 'has-errors': item.errors.length }">
        <div class="primary-content">
            <div class="controls">
                <span v-if="(! item.is_playing)" @click="$emit('play', item)">
                    <i class="fa fa-play"></i>
                </span>
                <span v-else @click="$emit('pause', item)">
                    <i class="fa fa-pause"></i>
                </span>
            </div>
            <div class="meta">
                <span>{{ item.content.name }}</span>
                <br>
                <a href="#" @click.prevent="$emit('visit', item.content, 'artist')">{{ item.content.artist_display }}</a>
                |
                <a href="#" @click.prevent="$emit('visit', item.content, 'release')">{{ item.content.release_display }}</a>
            </div>
            <div class="time">
                <small v-if="item.is_buffering">buff</small>
                <small v-if="(! item.is_buffering && item.is_playing)">{{ item.playhead_position_ms | ms_to_time }}</small>
                {{ item.duration | ms_to_time }}
            </div>
            <div class="actions">
                <span @click="remove(item, $event)">
                    <i class="fa fa-ban"></i>
                </span>
                <span @click="collect(item, $event)">
                    <i class="fa fa-plus"></i>
                </span>
            </div>
        </div>
        <div v-if="item.errors.length" class="errors">
            <div v-for="(item, index) in item.errors" :key="('error' + index)">
                <span>Error: {{ error.code }}</span>
                &mdash;
                <span>{{ error.info }}</span>
            </div>
        </div>
        <div v-if="item.is_playing" class="playhead" @click="seek(item, $event)" v-on:mouseover="seek_enter(item, $event)"  v-on:mouseleave="seek_leave(item, $event)">
            <div class="progress-container">
                <div class="progress-indicator" v-bind:style="{ width: position + '%' }"></div>
            </div>
            <div class="seek-container" v-bind:style="{ width: seek_position + '%' }"></div>
        </div>
    </div>
</template>

