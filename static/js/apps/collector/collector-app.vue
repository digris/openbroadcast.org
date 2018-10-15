<script src="./collector-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';

    /* */
    .collector-container {

    }

    .batch-collect {
        padding: 20px 6px;
        p {
            color: #fff;
        }
    }

    .item-to-collect {
        margin-top: 10px;
        //margin-bottom: 10px;
        color: #fff;
        padding: 6px;
        .item {

            background: rgba(#000, .9);
            display: flex;
            .visual {
                color: green;
                width: 64px;
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
        margin: 12px 0;
        padding: 6px;

        input {
            padding: 3px 6px;
            width: 98%;
            background: transparent;
            color: #fff;
            border: 1px solid #444444;
        }
    }

    .playlist-create {

        .input-container {

            label {
                color: #fff;
            }
            input {
                padding: 3px 6px;
                background: transparent;
                color: #fff;
                border: 1px solid #444444;
            }

        }
    }


</style>

<template>
    <modal :show="show_modal" :scope="scope" @close="show_modal=false">
        <div slot="content" class="collector-app collector-container">

            <div v-if="(items_to_collect.length > 1)" class="batch-collect">
                <p>
                    (( multiple)) {{ items_to_collect.length }}
                </p>
            </div>
            <div v-else v-for="item_to_collect in items_to_collect" class="item-to-collect">
                <div class="item">
                    <div class="visual">
                        <img v-bind:src="item_to_collect.content.image">
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
            <div class="foo">
                <div class="tabbed-navigation">
                    <div @click.prevent="set_scope('list')" v-bind:class="{ selected: (scope === 'list') }"
                         class="tab-selector">
                        <span>Your Playlists</span>
                    </div>
                    <div @click.prevent="set_scope('create')" v-bind:class="{ selected: (scope === 'create') }"
                         class="tab-selector">
                        <span>New Playlists</span>
                    </div>
                </div>


                <div v-if="(scope === 'list')" class="playlist-search">
                    <div class="input-container">
                        <input class="input-group-field"
                               type="text"
                               placeholder="Search playlists"
                               :value="query_string"
                               @input="update_query_string">
                    </div>
                    <div v-if="playlists" class="list-container">
                        <playlist
                            v-for="item in playlists"
                            v-bind:key="item.uuid"
                            v-bind:item="item"
                            @add="add_item_to_playlist(...arguments)"></playlist>
                    </div>
                </div>

                <div v-if="(scope === 'create')" class="playlist-create">
                    <div class="input-container">


                        <label for="playlist_create_name">Playlist title</label>


                        <input class="input-group-field"
                               id="playlist_create_name"
                               type="text"
                               placeholder="Playlist name"
                               :value="new_playlist_name"
                               @input="update_new_playlist_name">


                        <div>
                            <span>Playlist will be</span>

                            <input type="radio" id="playlist_create_type_private"
                                   name="type" value="basket">
                            <label for="playlist_create_type_private">private</label>

                            <input type="radio" id="playlist_create_type_public"
                                   name="type" value="public">
                            <label for="playlist_create_type_public">public</label>

                        </div>
                        <div>
                            <button @click.prevent="create_playlist" type="submit">Save</button>
                        </div>


                    </div>
                </div>


            </div>


        </div>
    </modal>
</template>
