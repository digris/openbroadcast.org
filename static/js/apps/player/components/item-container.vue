<script>
    export default {
        //name: 'item-container',
        props: [
            'item_to_play'
        ],
        data() {
            return {
                greeting: 'Hello'
            }
        },

        methods: {
            seek: function (item, e) {
                const x = e.clientX;
                const w = e.target.getBoundingClientRect().width;
                const p = Math.round((x / w) * 100);

                console.debug('$emit', 'seek', p, item)

                this.$emit('seek', item, p);
            },
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';
    .item-to-play {
        background: $primary-color-a;

        .item-to-play-header {
            color: blue;
        }

        .item-to-play-content {
            .item {
                color: #5a5a5a;
                background: $white;
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
                }
                .playhead{

                }
            }

        }

    }
</style>

<template>
    <div class="item-to-play">

        <div class="item-to-play-header">
            <span v-if="item_to_play">*{{ item_to_play.name }} - {{ item_to_play.ct }}*</span>
        </div>

        <div class="item-to-play-content">

            <div v-for="item in item_to_play.items" :key="item.uuid" class="item"  v-bind:class="{ 'is-playing': item.is_playing }">

                <div class="primary-content">
                    <div class="controls">
                        <span @click="$emit('play', item)">(( play ))</span>
                        <br>
                        <span @click="$emit('pause', item)">(( pause ))</span>
                    </div>

                    <div class="meta">
                        <!--<span>Playing: {{ item.is_playing }}{{ item.playhead_position }}</span><br>-->
                        <span>{{ item.content.name }}</span>
                        <br>
                        <span>{{ item.content.artist_display }}</span>
                        |
                        <span>{{ item.content.release_display }}</span>
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

                <div class="playhead" style="background: #999;" @click="seek(item, $event)">
                    <div v-if="item.is_playing" class="region" style="height: 10px; background: #000;" v-bind:style="{ width: (item.from_p + item.to_p) + '%', marginLeft: item.from_p + '%' }"></div>
                    <div class="region" style="height: 2px; background: #f00;" v-bind:style="{ width: (item.playhead_position) + '%'}"></div>
                </div>

            </div>

        </div>
    </div>
</template>
