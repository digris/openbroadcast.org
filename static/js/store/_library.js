/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';

const DEBUG = true;
const PLAYLIST_ENDPOINT = '/api/v2/library/playlist/';

const generateKey = function (objCt, objUuid) {
  return `${objCt}:${objUuid}`;
};

const state = {
  playlists: [],
};

const getters = {
  playlists: (state) => state.playlists,
  playlistsByUuid: (state) => (uuid) => {
    if (DEBUG) console.debug('getters - playlistsByUuid', uuid);
    return state.playlists.find((obj) => obj.uuid === uuid);
  },
};

const mutations = {
  setPlaylist: (state, { payload }) => {
    if (DEBUG) console.debug('mutations - setPlaylist', payload);

    const index = state.playlists.findIndex((obj) => obj.uuid === payload.uuid);
    if (index > -1) {
      Vue.set(state.playlists, index, payload);
    } else {
      state.playlists.push(payload);
    }
  },
};

const actions = {
  loadPlaylist: async (context, { uuid }) => {
    const url = `${PLAYLIST_ENDPOINT}${uuid}/`;
    APIClient.get(url).then((response) => {
      context.commit('setPlaylist', { payload: response.data });
    }).catch((e) => {
      console.warn('unable to load playlist', e);
    });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
