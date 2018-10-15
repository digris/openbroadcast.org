<script>

    import Loader from '../../../components/loader.vue';
    import {template_filters} from '../../../utils/template-filters';

    export default {
        props: [
            'item'
        ],
        components: {
            Loader
        },
        computed: {

        },
        methods: {

        },
        filters: template_filters,
    }
</script>

<style lang="scss" scoped>
    @import '../../../../sass/site/variables';
    // list styling
    .item {
        display: flex;
        position: relative;
        //margin-bottom: 6px;
        padding: 6px;
        border-bottom: 1px solid #444444;

        &:first-child {
            border-top: 1px solid #444444;
        }
        &:hover {
            background: rgba($primary-color-b, 0.2);
        }

        &.is-updated {
            // animation: highlight-change-bg .5s;
            .counts span {
                animation: highlight-change 3s;
            }
        }
        .visual {
            width: 64px;
            figure {
                margin: 0;
            }
        }
        .information {
            flex-grow: 1;
            padding: 6px 10px 0;
            color: #fff;
        }
        .actions {
            .button {
                border: 1px solid #a5a5a5;
                text-transform: uppercase;
                color: #a5a5a5;
                transition: border-radius 0.2s;
                &:hover {
                    background: $primary-color-b;
                    border-color: $primary-color-b;
                    color: #fff;
                    border-radius: 3px;

                }
            }
        }

        @keyframes highlight-change-bg {
            0% {
                background: transparent;
            }
            70% {
                background: $primary-color-b;
            }
            100% {
                background: transparent;
            }
        }

        @keyframes highlight-change {
            0% {
                background: $primary-color-b;
            }
            80% {
                background: $primary-color-b;
            }
            100% {
                background: transparent;
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
            <figure>
                <img v-if="(item.image)" v-bind:src="item.image"/>
                <img v-else
                     src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
                     width="120"
                     height="120">
            </figure>
        </div>
        <div class="information">
            <span class="name">
                 {{ item.name }}
            </span>
            <div v-if="item.series_display">
                <span>{{ item.series_display }}</span>
            </div>

            <div class="counts">
                <span>{{ item.duration | ms_to_time }}</span>
                &mdash;
                <span>{{ item.num_media }} tracks</span>
            </div>

        </div>
        <div class="actions">
            <div class="button-group">
                <a @click="$emit('add', item)"
                   class="button hollow">
                    Add
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
