<script>


import tabex from 'tabex';
import canAutoPlay from 'can-autoplay';

// import APIClient from '../../api/caseTranslatingClient';
// import PlayerBackend from './backend';

import PlayerToolbar from './PlayerToolbar.vue';
import PlayerPanel from './PlayerPanel.vue';
import PlayerControls from './PlayerControls.vue';
import PlayerList from './PlayerList.vue';
import PlayerFooter from './PlayerFooter.vue';

const DEBUG = true;

const exchange = tabex.client();

export default {
  name: 'Player',
  components: {
    'player-toolbar': PlayerToolbar,
    'player-panel': PlayerPanel,
    'player-controls': PlayerControls,
    'player-list': PlayerList,
    'player-footer': PlayerFooter,
  },
  props: {
    mode: {
      type: String,
      default: 'master',
    },
  },
  data() {
    return {
      masterWindow: null,
      canAutoplay: null,
      isLoading: false,
      controls: [],
    };
  },
  computed: {
    items() {
      return this.$store.getters['player/items'];
    },
    mediaList() {
      return this.$store.getters['player/mediaList'];
    },
    currentIndex() {
      return this.$store.getters['player/currentIndex'];
    },
    currentMedia() {
      return this.$store.getters['player/currentMedia'];
    },
    hasNext() {
      return this.$store.getters['player/hasNext'];
    },
    hasPrevious() {
      return this.$store.getters['player/hasPrevious'];
    },
  },
  mounted() {
    if (DEBUG) console.group('PlayerApp');

    exchange.on('player.heartbeat', this.receiveHeartbeat);
    exchange.on('player.controls', this.receiveControls);

    if (DEBUG) console.debug('mounted in master mode');
    this.masterWindow = window;

    canAutoPlay.audio().then(({ result }) => {
      if (result === true) {
        this.canAutoplay = true;
        if (DEBUG) console.info('can autoplay: YES');
      } else {
        this.canAutoplay = false;
        if (DEBUG) console.warn('can autoplay: NO');
      }
    });

    // const be = new PlayerBackend();
    // console.debug(be);

    this.sendHeartbeat({
      sender: 'master',
      receiver: 'slave',
      signal: 'ready',
    });

    // inform the 'slave(s)' in case of destruction
    window.addEventListener('beforeunload', (e) => {
      this.sendHeartbeat({
        sender: 'master',
        receiver: 'slave',
        signal: 'destroyed',
      });
    });


    if (DEBUG) console.groupEnd();

    this.onControls({
      do: 'load',
      opts: {
        offset: 0,
        mode: 'replace',
      },
      items: [
        {
          ct: 'alibrary.release',
          uuid: '0f7b084c-e89f-4fd2-9d67-e991bdf1ce34',
        },
      ],
    });
  },
  methods: {
    sendHeartbeat(payload) {
      payload.ts = Date.now();
      if (DEBUG) console.debug('sendHeartbeat', payload);
      exchange.emit('player.heartbeat', payload);
    },
    receiveHeartbeat(payload) {
      if (DEBUG) console.debug('receiveHeartbeat', payload);
    },
    receiveControls(payload) {
      if (DEBUG) console.debug('receiveControls', payload);
      this.controls = payload;
      // TODO: validate payload
      this.onControls(payload.action);
    },
    onControls(action) {
      if (DEBUG) console.debug('onControl', action);

      if (action.do === 'load') {
        this.isLoading = true;
        const payload = {
          items: action.items,
          replace: action.opts.mode === 'replace',
        };
        this.$store.dispatch('player/loadItems', payload).then((response) => {
          if (DEBUG) console.debug('loaded items', response);
          this.isLoading = false;
          console.info('playAtIndex', 0);
          this.playAtIndex(0);
        }, (error) => {
          console.error('onControls - error', error);
          this.isLoading = false;
        });
      }
    },
    playNext() {
      this.playAtIndex(this.currentIndex + 1);
    },
    playPrevious() {
      this.playAtIndex(this.currentIndex - 1);
    },
    // mapped vuex actions
    playAtIndex(index) {
      this.$store.dispatch('player/playAtIndex', { index });
    },

  },
};
</script>
<template>
  <div class="player">
    <player-toolbar class="player__toolbar">
      (( toolbar ))
    </player-toolbar>
    <player-panel class="player__panel">
      (( panel ))
    </player-panel>
    <player-controls
      class="player__controls"
      :has-next="hasNext"
      :has-previous="hasPrevious"
      @next="playNext"
      @previous="playPrevious"
    >
      (( controls ))
    </player-controls>
    <player-list
      class="player__list"
      :items="items"
    >
      (( list ))
    </player-list>
    <div style="display: none;">
      canAutoplay: {{ canAutoplay }}<br>
      currentIndex: {{ currentIndex }}<br>
      currentMedia: {{ currentMedia }}<br>
      mediaList: {{ mediaList.length }}<br>
      hasNext: {{ hasNext }}<br>
      hasPrevious: {{ hasPrevious }}<br>
      isLoading: {{ isLoading }}<br>
      controls: {{ controls }}<br>
    </div>
    <player-footer class="player__footer">
      (( footer ))
    </player-footer>
  </div>
</template>
<style lang="scss" scoped>

  .player {
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;

    /*color: var(--secondary-color);*/
    /*background: v(page-bg-color);*/

    &__toolbar {
      background: black;
    }

    &__panel {
      min-height: 100px;
      padding: 10px;
      background: $page-bg-color;
    }

    &__controls {
      height: 48px;

      // background: var(--primary-color);
    }

    &__list {
      flex-grow: 1;
      overflow-y: scroll;
      background: white;
    }

    &__footer {

    }

  }
</style>
