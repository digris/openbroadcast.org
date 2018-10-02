import Vue from 'vue';
import tabex from 'tabex';
import canAutoPlay from 'can-autoplay';
import soundmanager from 'soundmanager2/script/soundmanager2-html5';
import APIClient from '../../api/client';

import ItemContainer from './components/item-container.vue';
import Waveform from './components/waveform.vue'



const DEBUG = true;
const POPUP_SIZE = {width: 600, height: 800};


const exchange = tabex.client();


const pre_process_loaded_items = (results) => {

    results.forEach((item_to_play, i) => {
        item_to_play.items.forEach((item, j) => {
            item = pre_process_item(item);
            item.key = `${item.content.uuid}-${i}-${item_to_play.uuid}-${j}`;
            console.warn(item.key)
        });
    });

    return results;
};

const pre_process_item = (item) => {

    // set properties needed for display
    item.errors = [];
    item.is_playing = false;
    item.playhead_position = 0;
    item.playhead_position_ms = 0;

    // normalise duration to ms (sm2)
    item.duration = Math.floor(item.content.duration * 1000);

    // calculate cues & fades - API delivers them relative, for
    // player they are needed in absolute (ms) values
    item.from = (item.cue_in === undefined) ? 0 : item.cue_in;
    item.to = (item.cue_out === undefined) ? item.duration : item.duration - item.cue_out;

    // and in percentage for display
    item.from_p = Math.floor(item.from / item.duration * 100);
    item.to_p = Math.floor(item.to / item.duration * 100);
    item.duration_p = Math.floor((item.to - item.from) * 100);

    // absolute timestamps for fade
    item.fade_to = (item.fade_in === undefined) ? item.from : item.from + item.fade_in;
    item.fade_from = (item.fade_out === undefined) ? null : item.to - item.fade_out;

    console.log('processed item:', item);

    return item;
};

const reset_item = (item) => {

    // set properties needed for display
    item.is_playing = false;
    item.playhead_position = 0;
    item.playhead_position_ms = 0;

    return item;
};

const audio_level_for_position = (item, position) => {

    let level = 0.5;

    if (position <= item.from) {
        //console.debug('cue in > mute');
        level = 0
    }

    if (position >= item.to) {
        //console.debug('cue out > mute');
        level = 0
    }

    if (position >= item.fade_to && position < item.fade_from) {
        //console.debug('no fade or cue in progress > set to 1');
        level = 1
    }

    if (position > item.from && position < item.fade_to) {
        //console.debug('fade in');
        level = (position - item.from) / (item.fade_to - item.from);
    }

    if (position > item.fade_from && position < item.to) {
        //console.debug('fade out');
        level = (1 - (position - item.fade_from) / (item.to - item.fade_from));
    }


    // if(position <= item.from || position >= item.to) {
    //     return 0;
    // }
    //
    // if(position > item.fade_to || position < item.fade_from) {
    //     return 1;
    // }

    return level
};


//const PlayerApp = new Vue({
const PlayerApp = Vue.extend({
    /**************************************************************
     * player operates in two 'modes': master & slave
     * the 'master' is where the actual playing happens: the popup
     * all other windows/tabs act as 'slave' and send controls
     * to the 'master'
     **************************************************************/
    //name: 'PlayerApp',
    components: {
        ItemContainer,
        Waveform
    },
    data() {
        return {
            loading: false,
            master_window: null,
            heartbeat_payloads: [],
            action_payloads: [],

            items_to_play: [],
            // player backend
            player: null,
            volume: 90,
            can_autoplay: false,
            player_current_item: null,
            player_current_media: null,
            // player_playing: false
        }
    },

    computed: {
        player_playing: function () {
            return (this.player && this.player.playState === 1)
        },
        // media_list: function() {
        //     let all_media = [];
        //     this.items_to_play.forEach((item_to_play) => {
        //         item_to_play.items.forEach((media) => {
        //             all_media.push(media)
        //         });
        //     });
        //     return all_media;
        // },
        // next_sound: function (media) {
        //     // if no media given lookup is relative to 'player_current_media'
        //
        //     media = (media === undefined) ? this.player_current_media : media;
        //
        //     let index = this.media_list.findIndex((element) => {return element.media.uuid === media.uuid});
        //
        //     return index;
        //
        // },
    },
    filters: {
        sec_to_time: function (value) {
            return ms_to_time(value * 1000)
        },
        ms_to_time: function (value) {
            return ms_to_time(value)
        }
    },
    mounted: function () {
        if (DEBUG) console.group('PlayerApp');


        /**********************************************************
         * subscribe to local-storage based channels.
         * 'heartbeat' channel is used to handle/establish
         * inter-window communication - where the 'control' channel
         * handles player controls.
         **********************************************************/

        exchange.on('player.heartbeat', this.heartbeat_receive);
        exchange.on('player.controls', this.controls_receive);


        /**********************************************************
         * in 'master' mode the player sends a pingback / 'ready'
         * status to the slave(s).
         **********************************************************/

        if (DEBUG) console.debug('mounted in master mode');
        this.master_window = window;

        canAutoPlay.audio().then(({result}) => {
            if (result === true) {
                this.can_autoplay = true;
                console.warn('can autoplay: YES')
            } else {
                this.can_autoplay = false;
                console.warn('can autoplay: NO')
            }
        });

        this.initialize_player();

        this.heartbeat_send({
            sender: 'master',
            receiver: 'slave',
            signal: 'ready'
        });

        // set a periodic heartbeat - just in case...
        // setInterval(() => {
        //     this.heartbeat_send({
        //         sender: 'master',
        //         receiver: 'slave',
        //         signal: 'ready'
        //     });
        // }, 6000);

        // inform the 'slave(s)' in case of destruction
        window.addEventListener('beforeunload', (e) => {
            this.heartbeat_send({
                sender: 'master',
                receiver: 'slave',
                signal: 'destroyed'
            });
        });


        if (DEBUG) console.groupEnd();
    },

    methods: {

        /**********************************************************
         * hartbeat
         * wrapper around lsbridge to handle channel & timestamp
         **********************************************************/
        heartbeat_send: function (payload) {
            if (DEBUG) console.debug('heartbeat_send', payload);
            // for some reason we need to add a timestamp (resp. a changed value)
            // subsequent sending of identical data does not trigger 'receive'
            payload.ts = Date.now();
            //lsbridge.send(HEARTBEAT_NAMESPACE, payload);
            exchange.emit('player.heartbeat', payload);
        },

        /**********************************************************
         * hartbeat
         * not so elegant 'router' to handle master/slave scenario
         **********************************************************/
        heartbeat_receive: function (payload) {
            //if (DEBUG) console.info('heartbeat_receive_master', payload);
            if (payload.receiver !== 'master') {
                return;
            }

            if (payload.signal === 'ping') {
                if (DEBUG) console.info('ready signal received from slave - answer as ready');
                this.heartbeat_send({
                    sender: 'master',
                    receiver: 'slave',
                    signal: 'ready'
                });
            }

            this.heartbeat_payloads.push(payload)
        },

        /**********************************************************
         * controls
         * wrapper around lsbridge to handle channel & timestamp
         **********************************************************/
        controls_send: function (payload) {
            if (DEBUG) console.debug('controls_send', payload);
            payload.ts = Date.now();
            //lsbridge.send(CONTROLS_NAMESPACE, payload);
            exchange.emit('player.controls', payload);
        },
        controls_receive: function (payload) {
            if (DEBUG) console.debug('controls_receive', payload);
            if (this.is_slave) {
                return;
            }
            if (DEBUG) console.debug('controls_receive', payload);
            this.handle_action(payload.action);
        },


        /**********************************************************
         * send action to player (from 'local' or 'remote' source)
         **********************************************************/
        send_action: function (action) {
            if (DEBUG) console.debug('send_action', action);
            this.handle_action(action);
        },

        /**********************************************************
         * 'handle' action. this always happens in the 'master'
         **********************************************************/
        handle_action: function (action) {
            if (DEBUG) console.debug('handle_action', action);
            //this.action_payloads.push(action);
            this.action_payloads = [action]

            console.info(this.player);

            if (action.do === 'load') {
                // load playlist data from API

                this.items_to_play = [];

                const url = '/api/v2/player/play/';
                APIClient.put(url, {items: action.items})
                    .then((response) => {
                        console.log(response.data.results);
                        let results = pre_process_loaded_items(response.data.results);
                        this.items_to_play = results;

                        this.handle_action({
                            do: 'play',
                            item: results[0].items[0]
                        })

                    }, (error) => {
                        console.error('Player - error loading item', error)
                    });
            }

            if (action.do === 'pause') {
                this.player.pause();

                if (action.item) {
                    action.item.is_playing = false;
                    action.item.content.isrc = '-';
                }
            }

            if (action.do === 'seek') {
                this.player.setPosition(action.item.duration / 100 * action.value);
            }

            if (action.do === 'play') {


                if (this.player.paused) {
                    this.player.resume();
                } else {
                    this.player.pause();
                }

                if (action.item) {

                    const item = action.item;

                    console.debug('action.item', item);

                    this.player_current_media = item;

                    const opts = {
                        //url: 'http://local.openbroadcast.org:8080/media-asset/format/427d5dbc-6997-40a8-bebd-faa9a056ec7f/default.mp3',
                        //url: 'https://www.openbroadcast.org/media-asset/format/b92f4fc9-24e6-41e2-af9e-ac1fc8dbab84/default.mp3',
                        url: item.content.assets.stream,
                        // from: item.from,
                        // to: 20000,
                        // whileplaying: this.player_whileplaying
                        whileplaying: () => {
                            // item.duration = this.player.duration;
                            item.playhead_position = Math.round(this.player.position / item.duration * 10000) / 100;
                            item.playhead_position_ms = this.player.position;

                            if (this.player.position < item.from) {
                                //console.warn('reached cue out -> stopping', 'to:', item.to)
                                this.player.setPosition(item.from);
                            }
                            if (this.player.position > item.to) {
                                console.warn('reached cue out -> stopping', 'to:', item.to)
                                this.player.stop();
                                this.player_play_offset(1, item);
                            }

                            // get volume for current position
                            const audio_level = audio_level_for_position(item, this.player.position)

                            // console.debug('level for position:', audio_level, this.player.position);

                            this.player.setVolume(this.volume * audio_level);
                            //this.player.setVolume(50);

                            //item.playhead_position = Math.round(this.player.position / this.player.duration * 1000) / 10;
                        },
                        onfinish: () => {
                            this.player_play_offset(1, item);
                        },
                        onload: (a, b, c, d, e) => {
                            console.debug('onload:', a, b, c, d, e)
                        },
                        onerror: (error, info) => {
                            this.player.stop();
                            item.errors.push({
                                code: error,
                                info: info
                            });
                            console.error('onerror:', error, info)
                        }
                    };

                    this.player.play(opts);

                    this.player.setPosition(item.from);

                    // TODO: find a better way to set all other items to 'stopped'
                    this.items_to_play.forEach((item_to_play) => {
                        item_to_play.items.forEach((item) => {
                            item = reset_item(item);
                        });
                    });


                    item.is_playing = true;
                    item.content.isrc = '+';
                }

            }

        },

        player_whileplaying: function () {
            console.log(this.player.position, this.player.duration)
            console.log(this.player)
        },

        player_resume_blocked_autoplay: function () {
            console.warn('player_resume_blocked_autoplay');
            this.player.stop().play();
            this.can_autoplay = true;
        },

        player_play_offset: function (offset, media) {

            let all_media = [];
            this.items_to_play.forEach((item_to_play) => {
                item_to_play.items.forEach((media) => {
                    all_media.push(media)
                });
            });

            let index = all_media.findIndex((element) => element.key === media.key) + offset;

            if(index < 0 || index > (all_media.length - 1)) {
                return;
            }

            console.warn('player_get_next_sound', index);


            this.send_action({
                do: 'play',
                value: null,
                item: all_media[index]
            })

        },


        /**********************************************************
         * initialize player backend
         **********************************************************/
        initialize_player: function () {
            if (DEBUG) console.debug('initialize_player');
            // initialize soundmanager
            soundManager.setup({
                //preferFlash: false,
                forceUseGlobalHTML5Audio: true,
                html5PollingInterval: 100,
                debugMode: DEBUG,
                onready: (a, b, c, d) => {

                    // just simulating delay...
                    //setTimeout(() => {
                    this.player = soundManager.createSound({
                        multiShot: false,
                        id: 'player_app_player',
                        // whileplaying: self.backend.whileplaying,
                        // onbufferchange: self.backend.onbufferchange,
                        // onfinish: self.backend.onfinish

                        // onload: (a, b, c) => {
                        //     console.error('onload:', a, b, c);
                        // }

                    });
                }
            });
        },


        /**********************************************************
         * testing / debug....
         **********************************************************/
        player_controls: function (action, item, value) {
            if (DEBUG) console.debug('player_controls:', action, item, value);

            this.send_action({
                do: action,
                value: value === undefined ? null : value,
                // TODO: this likely will not work when emmited via local storage...
                item: item
            })
        },


        // player_control: function (a, b, c) {
        //     if (DEBUG) console.debug('player_control', a, b, c);
        // },


        player_load_from_api: function () {
            this.send_action({
                do: 'load',
                items: [
                    {
                        ct: 'alibrary.release',
                        uuid: '0068bec3-f08b-4b98-a476-1550d46c0271'
                    },
                    {
                        ct: 'alibrary.release',
                        uuid: '3e971e13-bcf6-49e7-ae0f-9f05c29a3bb1'
                    },
                    // {
                    //     ct: 'alibrary.playlist',
                    //     uuid: 'd856729f-9549-4411-b445-dcf42be56aca'
                    // }
                ]
            })
        },

        player_play_all: function () {
            console.log('player_play_all')
            let _items = [];
            $('[data-ct="release"][data-uuid]').each((i, el) => {
                let _item = {
                    ct: 'alibrary.release',
                    uuid: $(el).data('uuid')
                };
                //if (i < 4) {
                _items.push(_item)
                //}

            });

            this.send_action({
                do: 'load',
                items: _items
            })

        },

        player_pasue: function () {
            this.player.pause();
            setTimeout(() => {
                console.log('paused:', this.player)
            }, 1000)

        },

        player_resume: function () {
            this.player.resume();
            setTimeout(() => {
                console.log('resumed:', this.player)
            }, 1000)
        },

        player_play: function () {
            this.player.stop();


            //this.player.setPosition(5000);

            this.player.play({
                from: 5000,
                to: 10000,
                whileplaying: this.player_whileplaying
                // whileplaying: () => {
                //     console.log(this.player.position)
                // }
            })
            //this.player.stop();

            //this.player.play();
        },

        player_seek: function () {
            //this.player.setPosition(10000);
            this.player.stop().setPosition(10000).play();
        }


    }
});

module.exports = PlayerApp;
