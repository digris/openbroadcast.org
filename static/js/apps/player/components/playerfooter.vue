<script>

    import {tween} from 'shifty';
    import {templateFilters} from '../../../utils/template-filters';

    export default {
        props: [
            'items_to_play',
        ],
        data() {
            return {
                tweened_duration: 0
            }
        },
        components: {
        },
        computed: {
            duration: function() {
              let duration = 0;
                this.items_to_play.forEach((item_to_play) => {
                    item_to_play.items.forEach((item) => {
                        duration += item.duration;
                    });
                });
                return duration;
            },
            animated_duration: function () {
                return (this.tweened_duration === 0) ? this.duration : this.tweened_duration;
            },
        },
        watch: {
            number: function (newValue, oldValue) {
                tween({
                    from: {n: oldValue},
                    to: {n: newValue},
                    duration: 800,
                    easing: 'easeOutQuad',
                    step: (state) => {
                        this.tweened_num_media = state.n.toFixed(0);
                    }
                })
            },
            duration: function (newValue, oldValue) {
                tween({
                    from: {n: oldValue},
                    to: {n: newValue},
                    duration: 500,
                    easing: 'easeOutQuad',
                    step: (state) => {
                        this.tweened_duration = state.n.toFixed(0);
                    }
                })
            }
        },
        methods: {
            add_all_to_playlist: function () {
                let _items = [];
                this.items_to_play.forEach((item_to_play) => {
                    item_to_play.items.forEach((item) => {
                        _items.push(item)
                    });
                });
                const _e = new CustomEvent('collector:collect', {detail: _items});
                window.dispatchEvent(_e);
            },
        },
        filters: templateFilters,
    }
</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';
    .player-footer {
        border-top: 1px solid #eaeaea;
        padding: 3px 6px 1px 6px;
        display: flex;
        color: #fff;

        .information {
            flex-grow: 1;
        }
        .actions {
            .button {
                border: 1px solid $primary-color-b;
                text-transform: uppercase;
                color: $primary-color-b;
                transition: border-radius 0.2s;
                padding: 0 12px;
                &:hover {
                    background: $primary-color-b;
                    border-color: $primary-color-b;
                    color: #fff;
                    border-radius: 3px;
                    text-decoration: none;
                }
            }
        }

    }

</style>

<template>
    <div class="player-footer">
        <div class="information">
            Total: <span>{{ animated_duration | ms_to_time }}</span>
        </div>
        <div class="actions">
            <div class="button-group">
                <a @click.prevent="add_all_to_playlist"
                   class="button hollow">
                    Add all to playlist
                </a>
            </div>
        </div>
    </div>
</template>
