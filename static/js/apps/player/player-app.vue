<script src="./player-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';

    .player-app {
        background: white;
    }

    .player-container {
        display: flex; /* displays flex-items (children) inline */
        flex-direction: column; /* stacks them vertically */
        height: 100%; /* needs to take the parents height, alternative: body {display: flex} */

        header {
            background: #fff;
        }

        main {
            flex: 1; /* takes the remaining height of the "container" div */
            overflow: auto; /* to scroll just the "main" div */
        }

        footer {
            background: red;
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
            height: 24px;
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
            //border: 2px solid blue;
            background: #fff;
            //padding: 4px 4px 4px 24px;
            margin: 2px 0;
        }

    }




    .player-footer {
        border-top: 1px solid black;
    }

    /*
    .autoplay-container {
        background: $primary-color-b;
        display: flex;
        height: 100%;
        align-items: center;
        justify-content: center;
        flex-direction: row;
        .autoplay-panel {
            flex-grow: 1;
            flex-shrink: 1;
            flex-basis: auto;
            color: white;
            text-align: center;
        }
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
        flex-direction: row;
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
    }

    .loading-container {
        background: rgba(255, 255, 255, 0.8);
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
                            <a href="#">{{ player_current_media.content.name }}</a>
                            <br>
                            <a href="#">{{ player_current_media.content.artist_display }}</a>
                            <br>
                            <a href="#">{{ player_current_media.content.release_display }}</a>
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
                    <a v-on:click.prevent="player_controls('stop')">
                        <i class="fa fa-stop"></i>
                    </a>
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
                    <div v-for="item_to_play in items_to_play" v-bind:key="item_to_play.uuid">
                        <div class="item-to-play">
                            <span class="name">{{ item_to_play.name }}</span>
                        <media
                            v-for="item in item_to_play.items"
                            v-bind:key="item.key"
                            v-bind:item="item"
                            @play="player_controls('play', ...arguments)"
                            @pause="player_controls('pause', ...arguments)"
                            @seek="player_controls('seek', ...arguments)"
                        >
                        </media>
                        </div>
                    </div>
                </div>

                <div v-if="(! can_autoplay)" class="autoplay-container">
                    <div @click="player_resume_blocked_autoplay"  class="autoplay-panel">
                    <span @click="player_resume_blocked_autoplay" class="autoplay-button">
                        (( CLICK ME TO PLAY))
                    </span>
                        <br>
                        <span class="autoplay-info">
                        (( text about autoplay... ))
                    </span>
                    </div>
                </div>

                <div v-if="loading" class="loading-container">
                    <span class="loading-info">
                        (( loading ))
                    </span>
                </div>

            </div>
        </main>

        <footer>
            <div class="player-footer">
                (( footer ))
            </div>
        </footer>

    </div>

</template>
