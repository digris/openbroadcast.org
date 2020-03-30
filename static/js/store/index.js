import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import createMutationsSharer from 'vuex-shared-mutations';
import scheduler from './_scheduler';
import objectHistory from './_objectHistory';
import objectSelection from './_objectSelection';
import library from './_library';
import player from './_player';

Vue.use(Vuex);

export default new Vuex.Store({
  namespaced: true,
  modules: {
    scheduler,
    objectHistory,
    objectSelection,
    library,
    player,
  },
  state: {
    settings: {
      search_fuzzy_match_mode: false,
    },
  },
  mutations: {
    update_settings(state, obj) {
      state.settings[obj.key] = obj.value;
    },
  },
  actions: {},
  plugins: [
    createPersistedState({
      key: 'store',
      paths: [
        'settings',
        'scheduler.settings',
        'scheduler.clipboard',
      ],
    }),
    createMutationsSharer({
      predicate: [
        'scheduler/addToClipboard',
        'scheduler/clearClipboard',
      ],
    }),
  ],
});
