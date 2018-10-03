import Vue from 'vue';
import tabex from 'tabex';
import APIClient from '../../api/client';

const DEBUG = true;

const POPUP_SIZE = {width: 600, height: 800};


const exchange = tabex.client();


//const PlayerApp = new Vue({
const PlayerControlApp = Vue.extend({
    /**************************************************************
     *
     **************************************************************/
    data() {
        return {
            has_master: false,
            master_window: null,
            player_url: '/player-ng/',
            heartbeat_payloads: [],
            action_payloads: [],
            // just temporary
            enabled: false
        }
    },
    mounted: function () {
        if (DEBUG) console.group('PlayerControlApp');

        exchange.on('player.heartbeat', this.heartbeat_receive);
        //exchange.on('player.controls', this.controls_receive);


        /**********************************************************
         * in 'slave' mode the only action needed during
         * pageload is to send a 'ping' to the 'master'.
         * if the 'master' exists he will respond with a pingback.
         * if a 'slave' receives a pingback it will set 'has_master'
         * (out of the slave perspective.. :) ) to true.
         **********************************************************/

        if (DEBUG) console.debug('mounted');
        this.heartbeat_send({
            sender: 'slave',
            receiver: 'master',
            signal: 'ping'
        });

        if (DEBUG) console.groupEnd();


        // TODO: temporary: check if controls should be displayed
        // localStorage.setItem('_dev_player_enabled', 'yes');
        if(localStorage.getItem('_dev_player_enabled') === 'yes') {
            this.enabled = true;
        }

        if(this.enabled) {
            console.info('PlayerControlApp enabled (dev mode)');
            // remove play (click) handlers or 'old' player
            $('.playable.popup').removeClass('popup');
            // re-bind
            $(document).on('click', '.playable', (e) => {
                e.preventDefault();
                let el = $(e.currentTarget).parents('[data-uuid]');
                let ct = el.data('ct');
                if(ct.substring(0,9) !== 'alibrary.') {
                    ct = `alibrary.${ct}`;
                }
                this.send_action({
                    do: 'load',
                    items: [
                        {
                            ct: ct,
                            uuid: el.data('uuid')
                        },
                    ]
                })
            });

        } else {
            if (DEBUG) console.debug('PlayerControlApp disabled (dev mode)');
        }
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
        // controls_receive: function (payload) {
        //     if (DEBUG) console.debug('controls_receive', payload);
        //     if (this.is_slave) {
        //         return;
        //     }
        //     if (DEBUG) console.debug('controls_receive', payload);
        //     this.handle_action(payload.action);
        // },


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
                    // {
                    //     ct: 'alibrary.release',
                    //     uuid: '0068bec3-f08b-4b98-a476-1550d46c0271'
                    // },
                    // {
                    //     ct: 'alibrary.release',
                    //     uuid: '3e971e13-bcf6-49e7-ae0f-9f05c29a3bb1'
                    // },
                    {
                        ct: 'alibrary.playlist',
                        uuid: '197d9367-aa1c-4c7a-91d0-c4ea6875fd86'
                    },
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

    }
});

module.exports = PlayerControlApp;
