/* eslint no-shadow: ["error", { "allow": ["state", "getters"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
// eslint-disable-next-line no-unused-vars
// eslint-disable-next-line import/no-cycle
import store from '.';
import APIClient from '../api/caseTranslatingClient';

const DEBUG = false;
const PLAYER_ENDPOINT = '/api/v2/player/play/';

let backend = null;

const state = {
  items: [],
  playerState: 1,
  currentIndex: -1,
};

const getters = {
  items: (state) => state.items,
  playerState: (state) => state.playerState,
  currentIndex: (state) => state.currentIndex,
  currentMedia: (state, getters) => {
    if (state.currentIndex < 0) {
      return null;
    }
    return getters.mediaList[state.currentIndex];
  },
  mediaList: (state) => state.items.reduce((f, item) => f.concat(item.media), []),
  hasNext: (state, getters) => (state.currentIndex < (getters.mediaList.length - 1)),
  hasPrevious: (state) => state.currentIndex > 0,
};

const mutations = {
  setItems: (state, { payload }) => {
    if (DEBUG) console.debug('mutations - setItems', payload);
    state.items = payload;
  },
  addItems: (state, { payload }) => {
    if (DEBUG) console.debug('mutations - addItems', payload);
    // state.items.push(payload);
    state.items = [...state.items, ...payload];
  },
  setIndex: (state, { index }) => {
    if (DEBUG) console.debug('mutations - setIndex', index);
    state.currentIndex = index;
  },
};

const actions = {
  loadItems: async (context, { items, replace }) => {
    if (DEBUG) console.debug('actions - loadItems', items, replace);
    const url = `${PLAYER_ENDPOINT}`;
    const response = await APIClient.put(url, { items });
    if (replace) {
      context.commit('setItems', { payload: response.data.results });
    } else {
      context.commit('addItems', { payload: response.data.results });
    }

    return response;
  },
  playAtIndex: (context, { index }) => {
    console.info('backend', backend);
    if (DEBUG) console.debug('actions - playAtIndex', index);
    context.commit('setIndex', { index });
  },
  playByMediaObj: (context, { media }) => {
    if (DEBUG) console.debug('actions - playByMediaObj', media);
    const index = context.getters.mediaList.findIndex((obj) => obj === media);
    if (index > -1) {
      context.commit('setIndex', { index });
    }
  },
};

class PlayerBackend {
  // eslint-disable-next-line no-shadow
  constructor({ store }) {
    console.debug('PlayerBackend store', store);
    this.sound = null;
    soundManager.setup({
      forceUseGlobalHTML5Audio: true,
      html5PollingInterval: 100,
      debugMode: true,
      onready: () => {
        this.sound = soundManager.createSound({
          multiShot: false,
          id: 'player_backend_sm2',
        });
      },
    });
  }
}


setImmediate(() => {
  backend = new PlayerBackend({ store });
});

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
