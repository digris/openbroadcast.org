import Vue from 'vue';
import lsbridge from 'lsbridge';
import tabex from 'tabex';
import soundmanager from 'soundmanager2';
import APIClient from '../../api/client';

import ItemContainer from './components/item-container.vue'


const DEBUG = true;
const HEARTBEAT_NAMESPACE = 'player-heartbeat';
const CONTROLS_NAMESPACE = 'player-controls';

const POPUP_SIZE = {width: 600, height: 800};


const pre_process_loaded_items = (results) => {

    results.forEach((item_to_play) => {
        item_to_play.items.forEach((item) => {
            item = pre_process_item(item);
        });
    });

    return results;
};

const pre_process_item = (item) => {

    // set properties needed for display
    item.errors = []
    item.is_playing = false;
    item.playhead_position = 0;

    // normalise duration to ms (sm2)
    item.duration = Math.floor(item.content.duration * 1000);

    // calculate cues & fades - API delivers them relative, for
    // player they are needed in absolute (ms) values
    item.from = (item.cue_in === undefined) ? 0 : item.cue_in;
    item.to = (item.cue_out === undefined) ? item.duration : item.duration - item.cue_in -item.cue_out;

    // and in percentage for display
    item.from_p = Math.floor(item.from / item.duration * 100);
    item.to_p = Math.floor(item.to / item.duration * 100);


    console.log('processed item:', item);

    return item;
};

const reset_item = (item) => {

    // set properties needed for display
    item.is_playing = false;
    item.playhead_position = 0;

    return item;
};


const exchange = tabex.client();


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
        ItemContainer
    },
    data() {
        return {
            loading: false,
            name: 'foo',
            is_master: false,
            is_slave: false,
            has_master: false,
            master_window: null,
            player_url: '/player-ng/',
            heartbeat_payloads: [],
            action_payloads: [],

            items_to_play: [],
            // player backend
            player: null,
            // player_playing: false
        }
    },

    computed: {
        player_playing: function () {
            return (this.player && this.player.playState === 1)
        },
    },
    mounted: function () {
        if (DEBUG) console.group('PlayerApp');

        this.is_master = $('body').data('player-mode') === 'master';
        this.is_slave = !this.is_master;

        /**********************************************************
         * subscribe to local-storage based channels.
         * 'heartbeat' channel is used to handle/establish
         * inter-window communication - where the 'control' channel
         * handles player controls.
         **********************************************************/
        // lsbridge.subscribe(HEARTBEAT_NAMESPACE, this.heartbeat_receive);
        // lsbridge.subscribe(CONTROLS_NAMESPACE, this.controls_receive);

        // exchange.on('player.heartbeat', (payload) => {
        //     console.debug('exchange.on', payload)
        // });

        exchange.on('player.heartbeat', this.heartbeat_receive);
        exchange.on('player.controls', this.controls_receive);


        /**********************************************************
         * in 'slave' mode the only action needed during
         * pageload is to send a 'ping' to the 'master'.
         * if the 'master' exists he will respond with a pingback.
         * if a 'slave' receives a pingback it will set 'has_master'
         * (out of the slave perspective.. :) ) to true.
         **********************************************************/
        if (this.is_slave) {
            if (DEBUG) console.debug('mounted in slave mode');
            this.heartbeat_send({
                sender: 'slave',
                receiver: 'master',
                signal: 'ping'
            });
        }

        /**********************************************************
         * in 'master' mode the player sends a pingback / 'ready'
         * status to the slave(s).
         **********************************************************/
        if (this.is_master) {
            if (DEBUG) console.debug('mounted in master mode');
            this.master_window = window;

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
        }

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
            if (this.is_master) {
                this.heartbeat_receive_master(payload);
            }
            if (this.is_slave) {
                this.heartbeat_receive_slave(payload);
            }
        },

        heartbeat_receive_master: function (payload) {
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

        heartbeat_receive_slave: function (payload) {
            //if (DEBUG) console.info('heartbeat_receive_slave', payload);
            if (payload.receiver !== 'slave') {
                return;
            }

            if (payload.signal === 'ready') {
                if (DEBUG) console.info('ready signal received from master');
                this.has_master = true;
            }

            if (payload.signal === 'destroyed') {
                if (DEBUG) console.info('destroyed signal received from master');
                this.has_master = false;
            }

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

            /******************************************************
             * in master mode just pass the action to the handler
             ******************************************************/
            if (this.is_master) {
                this.handle_action(action);
                return;
            }

            /******************************************************
             * in slave mode popup situations must be handled
             ******************************************************/

            /******************************************************
             * 'master' directly attached, so the instance here
             * is the window 'opener'
             ******************************************************/
            if (this.master_window && !this.master_window.closed) {
                if (DEBUG) console.debug('master directly attached');
                this.controls_send({action: action});
                return;
            }

            /******************************************************
             * 'master' around, but not directly attached
             ******************************************************/
            if (this.has_master) {
                if (DEBUG) console.debug('looks like we have a master ready');
                this.controls_send({action: action});
                return;
            }

            /******************************************************
             * no 'master' detected - so a new window has to be
             * created, and action sent as soon as the window
             * is ready/loaded.
             ******************************************************/
            if (DEBUG) console.debug('no master arount. create a new player');
            const window_option = `width=${POPUP_SIZE.width},height=${POPUP_SIZE.height},titlebar=no,toolbar=no,location=no,status=no,menubar=no`;
            /// const window_option = '';
            this.master_window = window.open(this.player_url, 'Player App', window_option);
            this.master_window.onload = (e) => {
                this.controls_send({action: action});
            };

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

                    this.player.play({
                        //url: 'http://local.openbroadcast.org:8080/media-asset/format/427d5dbc-6997-40a8-bebd-faa9a056ec7f/default.mp3',
                        //url: 'https://www.openbroadcast.org/media-asset/format/b92f4fc9-24e6-41e2-af9e-ac1fc8dbab84/default.mp3',
                        url: item.content.assets.stream,
                        // from: item.from,
                        // to: 20000,
                        // whileplaying: this.player_whileplaying
                        whileplaying: () => {
                            // item.duration = this.player.duration;
                            action.item.playhead_position = Math.round(this.player.position / item.duration * 1000) / 10;
                            //action.item.playhead_position = Math.round(this.player.position / this.player.duration * 1000) / 10;
                        },
                        onerror: (error, info) => {
                            this.player.stop();
                            action.item.errors.push({
                                code: error,
                                info: info
                            });
                            console.error('onerror:', error, info)
                        }
                    });

                    this.player.setPosition(item.from);

                    // TODO: find a better way to set all other items to 'stopped'
                    this.items_to_play.forEach((item_to_play) => {
                        item_to_play.items.forEach((item) => {
                            item = reset_item(item);
                        });
                    });


                    action.item.is_playing = true;
                    action.item.content.isrc = '+';
                }

            }


            // this.player.play({
            //     //url: 'http://local.openbroadcast.org:8080/media-asset/format/427d5dbc-6997-40a8-bebd-faa9a056ec7f/default.mp3',
            //     url: 'https://www.openbroadcast.org/media-asset/format/b92f4fc9-24e6-41e2-af9e-ac1fc8dbab84/default.mp3',
            //     position: 500,
            //     whileplaying: this.player_whileplaying
            //     // whileplaying: () => {
            //     //     console.log(this.player.position)
            //     // }
            // })
        },

        player_whileplaying: function () {
            console.log(this.player.position, this.player.duration)
            console.log(this.player)
        },


        /**********************************************************
         * initialize player backend
         **********************************************************/
        initialize_player: function () {
            if (DEBUG) console.debug('initialize_player');
            // initialize soundmanager
            soundManager.setup({
                preferFlash: false,
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
                    });
                    //}, 2000);


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
                        uuid: 'b0edb06f-0a78-4ca0-8feb-620b31fc26ac'
                    },
                    {
                        ct: 'alibrary.playlist',
                        uuid: 'd856729f-9549-4411-b445-dcf42be56aca'
                    }
                ]
            })
        },

        player_play_all: function () {
            console.log('player_play_all')
            let _items =[];
            $('[data-ct="release"][data-uuid]').each((i, el) => {
                let _item = {
                    ct: 'alibrary.release',
                    uuid: $(el).data('uuid')
                };
                if(i < 4) {
                    _items.push(_item)
                }

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
