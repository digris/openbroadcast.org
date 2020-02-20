import Vue from 'vue';
import tabex from 'tabex';

import settings from '../../settings';

const DEBUG = true;

const POPUP_SIZE = { width: 400, height: 800 };


const exchange = tabex.client();

// const PlayerApp = new Vue({
const PlayerControlApp = Vue.extend({
  /** ************************************************************
     *
     ************************************************************* */
  data() {
    return {
      has_master: false,
      master_window: null,
      heartbeat_payloads: [],
      action_payloads: [],
    };
  },
  computed: {
    player_url: function () {
      if(settings.enableAlphaFeatures) {
        return '/player/next/';
      }
      return '/player/';
    }
  },
  mounted() {
    if (DEBUG) console.group('PlayerControlApp', settings);

    exchange.on('player.heartbeat', this.heartbeat_receive);
    // exchange.on('player.controls', this.controls_receive);


    /** ********************************************************
         * in 'slave' mode the only action needed during
         * pageload is to send a 'ping' to the 'master'.
         * if the 'master' exists he will respond with a pingback.
         * if a 'slave' receives a pingback it will set 'has_master'
         * (out of the slave perspective.. :) ) to true.
         ********************************************************* */

    if (DEBUG) console.debug('mounted');
    this.heartbeat_send({
      sender: 'slave',
      receiver: 'master',
      signal: 'ping',
    });

    if (DEBUG) console.groupEnd();


    /** ********************************************************
         * temporary for parallel legacy / ng situation
         ********************************************************* */
    console.info('PlayerControlApp enabled (dev mode)');

    // remove play (click) handlers or 'old' player
    $('.playable.popup').removeClass('popup');

    // re-bind legacy action handling
    $(document).on('click', '.playable, [data-playable]', (e) => {
      e.preventDefault();
      // let el = $(e.currentTarget).parents('[data-uuid]');
      const el = $(e.currentTarget);
      let ct = el.data('ct');
      const uuid = el.data('uuid');
      const mode = el.data('mode');
      const offset = el.data('offset') || 0;
      // TODO: propperly implement ctypes
      if (ct.substring(0, 9) !== 'alibrary.') {
        console.warn('depreciated ct - please always use "app.type" format.', ct);
        ct = `alibrary.${ct}`;
      }

      const items = [];

      if (uuid) {
        items.push({
          ct,
          uuid: el.data('uuid'),
        });
      } else {
        console.warn('no uuid provided');
        // TODO: a quick'n'dirty way to load items present on the current page
        $(`.item[data-ct="${ct}"]`).each((i, item) => {
          items.push({
            ct,
            uuid: $(item).data('uuid'),
          });
        });
      }

      this.send_action({
        do: 'load',
        opts: {
          mode,
          offset,
        },
        items,
      });
    });

    window.addEventListener('player:controls', (e) => {
      if (DEBUG) console.info('player:controls', e.detail);
      this.send_action(e.detail);
    }, false);
  },

  methods: {

    /** ********************************************************
         * hartbeat
         * wrapper around exxchange to handle channel & timestamp
         ********************************************************* */
    heartbeat_send(payload) {
      if (DEBUG) console.debug('heartbeat_send', payload);
      // for some reason we need to add a timestamp (resp. a changed value)
      // subsequent sending of identical data does not trigger 'receive'
      payload.ts = Date.now();
      exchange.emit('player.heartbeat', payload);
    },

    /** ********************************************************
         * hartbeat
         * not so elegant 'router' to handle master/slave scenario
         ********************************************************* */
    heartbeat_receive(payload) {
      // if (DEBUG) console.info('heartbeat_receive_slave', payload);
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

    /** ********************************************************
         * controls
         * wrapper around exchange to handle channel & timestamp
         ********************************************************* */
    controls_send(payload) {
      if (DEBUG) console.debug('controls_send', payload);
      payload.ts = Date.now();
      exchange.emit('player.controls', payload);
    },

    /** ********************************************************
         * send action to player (from 'local' or 'remote' source)
         ********************************************************* */
    send_action(action) {
      if (DEBUG) console.debug('send_action', action);

      /** ****************************************************
             * in master mode just pass the action to the handler
             ***************************************************** */
      if (this.is_master) {
        this.handle_action(action);
        return;
      }

      /** ****************************************************
             * in slave mode popup situations must be handled
             ***************************************************** */

      /** ****************************************************
             * 'master' directly attached, so the instance here
             * is the window 'opener'
             ***************************************************** */
      if (this.master_window && !this.master_window.closed) {
        if (DEBUG) console.debug('master directly attached');
        this.controls_send({ action });
        return;
      }

      /** ****************************************************
             * 'master' around, but not directly attached
             ***************************************************** */
      if (this.has_master) {
        if (DEBUG) console.debug('looks like we have a master ready');
        this.controls_send({ action });
        return;
      }

      /** ****************************************************
             * no 'master' detected - so a new window has to be
             * created, and action sent as soon as the window
             * is ready/loaded.
             ***************************************************** */
      if (DEBUG) console.debug('no master arount. create a new player');
      const window_option = `width=${POPUP_SIZE.width},height=${POPUP_SIZE.height},titlebar=no,toolbar=no,location=no,status=no,menubar=no`;
      // / const window_option = '';
      this.master_window = window.open(this.player_url, 'Player App', window_option);
      this.master_window.onload = (e) => {
        this.controls_send({ action });
      };
    },

    /** ********************************************************
         * testing / debug....
         ********************************************************* */
    player_controls(action, item, value) {
      if (DEBUG) console.debug('player_controls:', action, item, value);

      this.send_action({
        do: action,
        value: value === undefined ? null : value,
        // TODO: this likely will not work when emmited via local storage...
        item,
      });
    },

    player_play_all() {
      const _items = [];
      $('.playable[data-mode="replace"][data-ct="release"][data-uuid]').each((i, el) => {
        const _item = {
          ct: 'alibrary.release',
          uuid: $(el).data('uuid'),
        };
        _items.push(_item);
      });

      this.send_action({
        do: 'load',
        items: _items,
      });
    },

  },
});

export default PlayerControlApp;
