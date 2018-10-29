<script src="./player-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';

    .player-app {
        background: white;
    }

    .player-container {
        display: flex;
        flex-direction: column;
        height: 100%;

        header {
            background: #fff;
        }

        main {
            flex: 1;
            overflow: auto;
        }

        footer {
            height: 24px;
        }

    }

    .player-current-item {
        min-height: 132px;
        .primary-content {
            display: flex;
            padding: 10px;
            .meta {
                flex-grow: 1;
            }
            .visual {
                img {
                    width: 80px;
                    height: 80px;
                }
            }
        }
        .plahead {
            height: 30px;
            img {
                height: 32px;
                width: 100%;
            }
        }
    }

    .player-current-item-loading {
        min-height: 112px;
        background: $primary-color-b;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 150%;
        font-weight: 300;

    }

    .player-controls {
        //border-top: 1px solid black;
        padding: 4px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        .button-panel .fa {
            font-size: 20px;
            color: #a5a5a5;
            margin: 0 4px;
        }
    }

    .player-content {
        position: relative;
        //border-top: 1px solid black;
        //border-bottom: 1px solid black;
        flex-direction: column; /* stacks them vertically */
        height: 100%; /* needs to take the parents height, alternative: body {display: flex} */


        .item-to-play {
            background: #fff;
            margin: 0 0 10px;

            .header {
                padding: 2px 2px 2px 5px;
                background: #fff;
                border-top: 1px solid #eaeaea;
                border-bottom: 1px solid #eaeaea;
            }
        }

    }

    /*
    .player-footer {
        border-top: 1px solid #eaeaea;
        padding: 2px 2px 0 5px;
    }
    */

    .autoplay-container {
        background: $primary-color-b;
        position: fixed;
        top: 0;
        height: 100%;
        width: 100%;
        z-index: 99;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        .autoplay-panel {
            cursor: pointer;
            width: 240px;
            height: 240px;
            border-radius: 120px;
            background: white;
            /*flex-grow: 1;*/
            /*flex-shrink: 1;*/
            flex-basis: auto;
            color: $primary-color-b;;
            text-align: center;
            align-items: center;
            display: flex;
            justify-content: center;
            flex-direction: row;
        }
        .autoplay-info {
            display: block;

            p {
                text-align: center;
                max-width: 320px;
                padding: 0;
                margin-top: 20px;
                color: white;
            }

        }
    }

    .loading-container {
        background: rgba(255, 255, 255, 0.9);
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
        transition: all .05s;
    }

    .fade-leave-active {
        transition: all .3s;
    }

    .fade-enter, .fade-leave-to {
        opacity: 0;
    }


</style>

<template>

    <div class="player-app player-container">

        <div class="player-overlay" v-if="(!player)">
            <div class="initialising" v-if="(!player)">
                <p>Initialising player.<br>Please be patient.</p>
            </div>
        </div>

        <header>
            <div class="player-current-item">

                <div v-if="player_current_media" v-bind:key="player_current_media.content.uuid">
                    <div class="primary-content">
                        <div class="meta">
                            <a href="#" @click.prevent="visit(player_current_media.content)">{{ player_current_media.content.name }}</a>
                            <br>
                            <a href="#" @click.prevent="visit(player_current_media.content, 'artist')">{{ player_current_media.content.artist_display }}</a>
                            <br>
                            <a href="#" @click.prevent="visit(player_current_media.content, 'release')">{{ player_current_media.content.release_display }}</a>
                        </div>

                        <div class="visual">
                            <img v-bind:src="player_current_media.content.image">
                        </div>
                    </div>

                    <div class="plahead">
                        <waveform
                            v-bind:key="player_current_media.uuid"
                            v-bind:item="player_current_media"
                            @seek="player_controls('seek', ...arguments)"></waveform>
                    </div>

                </div>
                <div v-else class="player-current-item-loading">
                    loading...
                </div>
            </div>


            <div class="player-controls">
                <div class="button-panel">
                    <a v-on:click.prevent="player_play_offset(-1, player_current_media)">
                        <i class="fa fa-step-backward"></i>
                    </a>
                    <!--
                    <a v-on:click.prevent="player_controls('stop')">
                        <i class="fa fa-stop"></i>
                    </a>
                    -->
                    <a v-on:click.prevent="player_controls('pause')">
                        <i class="fa fa-pause"></i>
                    </a>
                    <a v-on:click.prevent="player_controls('play')">
                        <i class="fa fa-play"></i>
                    </a>
                    <a v-on:click.prevent="player_play_offset(1, player_current_media)">
                        <i class="fa fa-step-forward"></i>
                    </a>
                </div>
            </div>
        </header>

        <main>
            <div class="player-content">

                <div v-if="(items_to_play && can_autoplay )" class="items-to-play">
                    <div v-for="item_to_play in items_to_play" v-bind:key="item_to_play.uuid" v-if="(item_to_play.items && item_to_play.items.length > 0)">
                        <transition name="fade">
                            <div class="item-to-play">

                                <div class="header">
                                    <span class="name">{{ item_to_play.name }}<!-- {{ item_to_play.ct }}--></span>
                                </div>

                                <media
                                    v-for="item in item_to_play.items"
                                    v-bind:key="item.key"
                                    v-bind:item="item"
                                    @play="player_controls('play', ...arguments)"
                                    @pause="player_controls('pause', ...arguments)"
                                    @seek="player_controls('seek', ...arguments)"
                                    @remove="player_controls('remove', ...arguments)"
                                    @visit="visit(...arguments)"></media>
                            </div>
                        </transition>
                    </div>
                </div>


                <transition name="fade">
                    <div v-if="(! can_autoplay)" class="autoplay-container">
                        <div @click="player_resume_blocked_autoplay"  class="autoplay-panel">
                            <span @click="player_resume_blocked_autoplay" class="autoplay-button">
                                Click to play
                            </span>
                        </div>

                        <div class="autoplay-info">
                            <p>
                                Your browser prevents audio from automatically playing.<br>
                                When opening the Open Broadcast player for the first time you have
                                to manually start the playback.
                            </p>
                        </div>

                    </div>
                </transition>

                <transition name="fade">
                    <div v-if="loading" class="loading-container">
                        <span class="loading-info">
                            <loader></loader>
                        </span>
                    </div>
                </transition>

            </div>
        </main>

        <footer>
            <playerfooter v-bind:items_to_play="items_to_play"></playerfooter>

            <!--
            <div class="player-footer">
                (( footer )) <span @click="add_all_to_playlist">Add all</span>
            </div>
            -->
        </footer>

    </div>

</template>
