import Vue from 'vue';
import tabex from 'tabex';
import canAutoPlay from 'can-autoplay';
import NoSleep from 'nosleep.js';
import soundmanager from 'soundmanager2/script/soundmanager2-html5';
import APIClient from '../../api/client';
import {visit_by_resource} from '../../utils/visit-by-resource';

import ItemContainer from './components/item-container.vue';
import Waveform from './components/waveform.vue'
import Media from './components/media.vue'
import Playerfooter from './components/playerfooter.vue'
import Loader from '../../components/ui/Loader.vue'

const DEBUG = true;

const exchange = tabex.client();
const noSleep = new NoSleep();

const pre_process_loaded_items = (results) => {

    results.forEach((item_to_play, i) => {
        item_to_play.items.forEach((item, j) => {
            item = pre_process_item(item);
            item.key = `${item.content.uuid}-${i}-${item_to_play.uuid}-${j}`;
        });
    });

    return results;
};

const pre_process_item = (item) => {

    // set properties needed for display
    item.errors = [];
    item.is_playing = false;
    item.is_buffering = false;
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
    item.fade_from = (item.fade_out === undefined) ? item.to : item.to - item.fade_out;

    // console.table({
    //     duration: item.duration,
    //     from: item.from,
    //     to: item.to,
    //     fade_to: item.fade_to,
    //     fade_from: item.fade_from,
    // });

    //console.log('processed item:', item);

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
        Media,
        Playerfooter,
        Waveform,
        Loader
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
                if (DEBUG) console.info('can autoplay: YES')
            } else {
                this.can_autoplay = false;
                if (DEBUG) console.warn('can autoplay: NO')
            }
        });

        this.initialize_player();

        this.heartbeat_send({
            sender: 'master',
            receiver: 'slave',
            signal: 'ready'
        });

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
            this.action_payloads = [action];

            console.info(this.player);

            if (action.do === 'load') {
                // load playlist data from API
                this.loading = true;

                const opts = action.opts || {};
                let mode = opts.mode || 'replace';
                let offset = opts.offset || 0;

                const url = '/api/v2/player/play/';
                APIClient.put(url, {items: action.items})
                    .then((response) => {
                        console.log(response.data.results);

                        this.loading = false;
                        let results = pre_process_loaded_items(response.data.results);


                        if (mode === 'replace') {
                            this.items_to_play = results;
                            this.handle_action({
                                do: 'play',
                                item: results[0].items[offset]
                            })
                        }

                        if (mode === 'queue') {
                            this.items_to_play = this.items_to_play.concat(results);
                        }

                    }, (error) => {
                        console.error('Player - error loading item', error);
                        this.loading = false;
                    });
            }

            if (action.do === 'stop') {
                this.player.pause().setPosition(action.item.from);

                if (action.item) {
                    action.item.is_playing = false;
                }
            }

            if (action.do === 'pause') {
                this.player.pause();

                if (action.item) {
                    action.item.is_playing = false;
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
                        whileplaying: () => {

                            // TODO: hack - assume browser can autoplay if playing...
                            if (!this.can_autoplay && this.player.position > 10) {
                                this.can_autoplay = true;
                            }

                            // item.duration = this.player.duration;
                            item.playhead_position = Math.round(this.player.position / item.duration * 10000) / 100;
                            item.playhead_position_ms = this.player.position;
                            item.is_buffering = this.player.isBuffering;

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
                            // item.errors.push({
                            //     code: error,
                            //     info: info
                            // });
                            item.errors = [{
                                code: error,
                                info: info
                            }];
                            console.error('onerror:', error, info);
                            this.player_play_offset(1, item);
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

                }

            }

            if (action.do === 'remove') {

                // TODO: find a better way to remove item
                this.items_to_play.forEach((item_to_play) => {
                    item_to_play.items.forEach((item, index) => {
                        if(item.key === action.item.key) {
                            console.warn('delete:', item.key, index)
                            if(item.is_playing) {
                                alert('cannot remove playing item')
                            } else {
                                Vue.delete(item_to_play.items, index)
                            }
                        }
                    });
                });

            }

        },

        player_whileplaying: function () {
            console.log(this.player.position, this.player.duration);
            console.log(this.player);
        },

        player_resume_blocked_autoplay: function () {

            if(this.items_to_play.length > 0 && this.items_to_play[0].items.length > 0) {
                this.handle_action({
                    do: 'play',
                    item: this.items_to_play[0].items[0]
                });
            }

            this.can_autoplay = true;

            noSleep.enable();
        },

        player_play_offset: function (offset, media) {

            let all_media = [];
            this.items_to_play.forEach((item_to_play) => {
                item_to_play.items.forEach((media) => {
                    all_media.push(media)
                });
            });

            let index = all_media.findIndex((element) => element.key === media.key) + offset;

            if (index < 0 || index > (all_media.length - 1)) {
                console.warn('player_play_offset index not available', index);
                this.player.stop();
                if (this.player_current_media) {
                    media.is_playing = false;
                    this.player_current_media.is_playing = false;
                }
                return;
            }

            console.log('player_get_next_sound', index);


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
            soundManager.setup({
                forceUseGlobalHTML5Audio: true,
                html5PollingInterval: 100,
                debugMode: DEBUG,
                onready: () => {
                    this.player = soundManager.createSound({
                        multiShot: false,
                        id: 'player_app_player',
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


        /**********************************************************
         * visit item detail
         **********************************************************/
        visit: visit_by_resource,
        // visit: function (content, scope) {
        //     if (DEBUG) console.debug('visit:', content, scope);
        //
        //     const url = (scope === undefined) ? content.url : content[scope];
        //
        //     APIClient.get(url)
        //         .then((response) => {
        //             console.log(response.data);
        //
        //             const detail_url = response.data.detail_url;
        //
        //             if (DEBUG) console.debug('visit:', detail_url);
        //
        //             if (window.opener) {
        //                 window.opener.location.href = detail_url;
        //                 window.opener.focus();
        //             }
        //
        //         }, (error) => {
        //             console.error('Player - error loading item', error);
        //         });
        // },


        // player_control: function (a, b, c) {
        //     if (DEBUG) console.debug('player_control', a, b, c);
        // },

        // add_all_to_playlist: function () {
        //     let _items = [];
        //
        //     // TODO: find a better way to set all other items to 'stopped'
        //     this.items_to_play.forEach((item_to_play) => {
        //         item_to_play.items.forEach((item) => {
        //             _items.push(item)
        //         });
        //     });
        //
        //     const _e = new CustomEvent('collector:collect', {detail: _items});
        //     window.dispatchEvent(_e);
        //
        // },


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
