<script>

    import {tween} from 'shifty';
    import Loader from '../../../components/loader.vue';
    import Visual from '../../../components/visual.vue';
    import {template_filters} from '../../../utils/template-filters';

    export default {
        props: [
            'item',
            'items_to_collect',
            'actions',
        ],
        data() {
            return {
                number: 10000,
                tweened_num_media: 0,
                tweened_duration: 0
            }
        },
        components: {
            Loader,
            Visual
        },
        computed: {
            in_playlist: function() {
              if(! this.items_to_collect || this.items_to_collect.length !== 1) {
                  return false
              }

              const content = this.items_to_collect[0].content;
              return this.item.item_appearances.includes(`${content.ct}:${content.uuid}`);

            },
            animated_duration: function () {
                return (this.tweened_duration === 0) ? this.item.duration : this.tweened_duration;
            },
            animated_num_media: function () {
                return this.tweened_num_media;
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
            'item.duration': function (newValue, oldValue) {
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
        methods: {},
        filters: template_filters,
    }
</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';
    // list styling
    .item {
        display: flex;
        position: relative;
        padding: 6px;
        border-bottom: 1px solid #444444;

        &:first-child {
            border-top: 1px solid #444444;
        }
        &:hover {
            background: rgba($primary-color-b, 0.2);
        }

        .visual {
            width: 52px;
            figure {
                margin: 0;
            }
        }
        .information {
            flex-grow: 1;
            padding: 0 10px 0;
            color: #fff;
            .name {
                color: #fff;
                text-decoration: none;
                &:hover {
                    text-decoration: underline;
                }
            }
        }
        .actions {

            .button-group {
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .button {
                border: 1px solid #a5a5a5;
                text-transform: uppercase;
                color: #a5a5a5;
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

        // TODO: make loading container more generic
        .loading-container {
            background: #222;
            position: absolute;
            height: 100%;
            width: 100%;
            top: 0;
            left: 0;
            z-index: 99;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: row;
        }
        .fade-enter-active {
            transition: all .05s;
        }
        .fade-leave-active {
            transition: all .1s;
        }
        .fade-enter, .fade-leave-to {
            opacity: 0;
        }
    }

</style>

<template>
    <div :key="item.uuid" class="item" v-bind:class="{ 'is-loading': item.loading, 'is-updated': item.updated }">
        <div class="visual">
            <visual v-bind:url="item.image"></visual>
        </div>
        <div class="information">
            <a class="name" href="#" @click.prevent="$emit('visit', item)">
                <i v-if="in_playlist" class="fa fa-star"></i>
                {{ item.name }}
            </a>
            <div v-if="item.series_display">
                <span>{{ item.series_display }}</span>
            </div>
            <div class="counts">
                <span>{{ animated_duration | ms_to_time }}</span>
                &mdash;
                <span>{{ item.num_media }} tracks</span>
            </div>
        </div>
        <div class="actions">
            <div class="button-group">
                <a v-if="(actions.indexOf('add') > -1)" @click="$emit('add', item)"
                   class="button hollow">
                    Add
                </a>
                <a v-if="(actions.indexOf('visit') > -1)" @click="$emit('visit', item)"
                   class="button hollow">
                    Visit playlist
                </a>
            </div>
        </div>
        <transition name="fade">
            <div v-if="item.loading" class="loading-container">
                <span class="loading-info">
                    <loader></loader>
                </span>
            </div>
        </transition>
    </div>
</template>
