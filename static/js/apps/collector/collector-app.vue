<script src="./collector-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';

    // custom scroll-bar
    @mixin custom-scroll-bar() {
        &::-webkit-scrollbar {
            border-radius: 0;
            height: 10px;
            width: 4px;
        }

        &::-webkit-scrollbar-thumb {
            background: #fff;
            border-radius: 0;
        }

        &::-webkit-scrollbar-track {
            border-radius: 0;
        }
    }

    .collector-container {
        display: flex;
        flex-direction: column;
        height: 100%;

        header {

        }

        .content-container {
            flex: 1;
            display: flex;
        }

    }

    .batch-collect {
        padding: 20px 6px;
        p {
            color: #fff;
        }
    }

    .item-to-collect {
        margin-top: 10px;
        margin-bottom: 10px;
        color: #fff;
        padding: 6px;
        .item {
            // background: rgba(#000, .9);
            display: flex;
            .visual {
                width: 52px;
                figure {
                    margin: 0;
                }
            }
            .information {
                flex-grow: 1;
                padding: 2px 10px;
            }
        }
    }

    .settings-container {
        padding: 0 6px 6px 80px;
        .setting {
            display: flex;
            label {
                color: rgba(255, 255, 255, 0.7);
                padding-left: 10px;
                margin-top: 4px;
            }
            input {
                //position: relative;
            }
        }
    }

    .tabbed-navigation {
        display: flex;
        border-bottom: 1px solid $primary-color-b;
        .tab-selector {
            flex-grow: 1;
            text-align: center;
            color: #fff;
            padding: 2px;
            cursor: pointer;
            text-transform: uppercase;
            margin: 0 6px;
            &:not(:last-child) {
                margin-right: 1px;
            }

            &:hover {
                background: #000;
            }

            &.selected {
                background: $primary-color-b;
            }
        }
    }

    .playlist-search .input-container {

    }

    .playlist-search {

        display: flex;
        flex-grow: 1;
        flex-direction: column;
        height: 100%;

        .input-container {

            margin: 12px 0;
            padding: 6px;

            .input-group {
                .input-group-field {
                    box-sizing: border-box;
                    padding-left: 6px;
                    height: 26px;
                    width: 100%;
                    background: transparent;
                    color: #fff;
                    border: 1px solid #444444;
                }
            }

        }

        .list-container {
            @include custom-scroll-bar;
            flex: 1;
            overflow: auto;
        }

    }

    .playlist-create {
        width: 100%;
        position: relative;

        .playlist-created-container {
            margin-top: 20px;
        }

        .input-container {

            margin: 12px 0;
            padding: 6px;

            .input-group {

                margin-bottom: 12px;

                .title {
                    color: rgba(255, 255, 255, 0.7);
                }

                label {
                    color: #fff;
                }

                .input-group-field {
                    box-sizing: border-box;
                    padding-left: 6px;
                    height: 26px;
                    width: 100%;
                    background: transparent;
                    color: #fff;
                    border: 1px solid #444444;
                }

                &.submit {
                    padding: 20px 0 0 0;
                    text-align: center;

                    .button {
                        border: 2px solid $primary-color-b;
                        background: #fff;
                        text-transform: uppercase;
                        color: $primary-color-b;
                        transition: border-radius 0.2s;
                        padding: 6px 24px;

                        &:hover {
                            background: $primary-color-b;
                            color: #fff;
                            border-radius: 4px;
                            text-decoration: none;
                        }
                    }

                }

            }

            .horizontal-radio-group {
                display: flex;
                justify-content: center;
                align-items: center;

                .title {
                    margin-right: 20px;
                }

                label {
                    display: flex;
                    color: rgba(255, 255, 255, 0.7);
                    margin: 0 20px 0 0
                }

                input {
                    margin-right: 6px;
                }
            }

            .form-errors {
                color: orangered;
                text-align: center;
            }

        }
    }

    .loading-container {
        background: rgba(34, 34, 34, 1);
        position: absolute;
        top: 0;
        height: 100%;
        width: 100%;
        z-index: 99;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: row;

    }

    .fade-enter-active {
        transition: all .5s;
    }

    .fade-leave-active {
        transition: all 0.5s;
    }

    .fade-enter, .fade-leave-to {
        opacity: 0;
    }

</style>

<template>
    <modal :show="show_modal" :scope="scope" @close="show_modal=false">
        <div slot="content" class="collector-app collector-container">
            <header>
                <div v-if="(items_to_collect && items_to_collect.length > 1)" class="batch-collect">
                    <p>
                        (( multiple)) {{ items_to_collect.length }}
                    </p>
                </div>
                <div v-else v-for="item_to_collect in items_to_collect" class="item-to-collect">
                    <div class="item">
                        <div class="visual">
                            <visual v-bind:url="item_to_collect.content.image"></visual>
                        </div>
                        <div class="information">
                            {{ item_to_collect.content.name }}
                            <br>
                            {{ item_to_collect.content.artist_display }}
                            |
                            {{ item_to_collect.content.release_display }}
                            <br>
                            {{item_to_collect.duration | ms_to_time}}
                        </div>
                    </div>
                </div>
                <!--
                <div class="settings-container">
                    <div class="setting">
                        <input type="checkbox" id="copy_cue_and_fade" value="html-news" name="user-age"> <label
                        for="copy_cue_and_fade">Copy cue and fade</label>
                    </div>
                </div>
                -->
                <div class="tabbed-navigation">
                    <div @click.prevent="set_scope_list" v-bind:class="{ selected: (scope === 'list') }"
                         class="tab-selector">
                        <span>Your Playlists</span>
                    </div>
                    <div @click.prevent="set_scope_create" v-bind:class="{ selected: (scope === 'create') }"
                         class="tab-selector">
                        <span>New Playlist</span>
                    </div>
                </div>
            </header>

            <div class="content-container">

                <div v-if="(scope === 'list')" class="playlist-search">
                    <div class="input-container">
                        <div class="input-group">
                            <input class="input-group-field"
                                   type="text"
                                   placeholder="Search playlists"
                                   :value="query_string"
                                   @input="update_query_string">
                        </div>
                    </div>
                    <div v-if="playlists" class="list-container scrollable">
                        <playlist
                            v-for="item in playlists"
                            v-bind:key="item.uuid"
                            v-bind:item="item"
                            v-bind:items_to_collect="items_to_collect"
                            v-bind:actions="['add', 'add-and-close']"
                            @visit="visit(...arguments)"
                            @add="add_item_to_playlist(...arguments)"></playlist>
                    </div>
                </div>

                <div v-if="(scope === 'create')" class="playlist-create">

                    <transition name="fade">
                        <div v-if="create_playlist_data.created" class="playlist-created-container">
                            <playlist
                                v-bind:key="create_playlist_data.created.uuid"
                                v-bind:item="create_playlist_data.created"
                                v-bind:items_to_collect="items_to_collect"
                                v-bind:actions="['visit']"
                                @visit="visit(...arguments)">
                                </playlist>
                        </div>
                    </transition>

                    <form v-if="(! create_playlist_data.created)" @submit.prevent="create_playlist">
                        <div class="input-container">
                            <div class="input-group">
                                <label for="playlist_create_name">Playlist title *</label>
                                <input class="input-group-field"
                                       id="playlist_create_name"
                                       ref="playlist_create_name"
                                       type="text"
                                       autofocus
                                       autocomplete="off"
                                       v-model="create_playlist_data.name">
                            </div>
                            <div class="input-group">
                                <div class="horizontal-radio-group">
                                    <span class="title">Playlist will be</span>
                                    <label>
                                        <input v-model="create_playlist_data.type" type="radio" name="type"
                                               value="basket"/>private
                                    </label>

                                    <label>
                                        <input v-model="create_playlist_data.type" type="radio" name="type"
                                               value="playlist"/>public
                                    </label>
                                </div>
                            </div>

                            <div v-if="create_playlist_data.errors.length" class="form-errors">
                                <span>Please correct the following error(s):</span>
                                <ul>
                                    <li v-for="error in create_playlist_data.errors">{{ error }}</li>
                                </ul>
                            </div>

                            <div class="input-group submit">
                                <input type="submit" value="Save" class="button">
                            </div>
                        </div>
                    </form>

                    <transition name="fade">
                        <div v-if="loading" class="loading-container">
                            <span class="loading-info">
                                <loader></loader>
                            </span>
                        </div>
                    </transition>


                </div>
            </div>

        </div>
    </modal>
</template>
