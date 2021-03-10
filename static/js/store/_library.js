/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
/* eslint max-len: [2, 120, 4] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';

const LIBRARY_ENDPOINT = '/api/v2/alibrary/';

const state = {
  playlists: [],
  mediaAppearances: {},
};

const getters = {
  playlists: (state) => state.playlists,
  playlistsByUuid: (state) => (uuid) => state.playlists.find((obj) => obj.uuid === uuid),
  mediaAppearancesByUuid: (state) => (uuid) => state.mediaAppearances[uuid] || {},
};

const mutations = {
  SET_PLAYLIST: (state, { payload }) => {
    const index = state.playlists.findIndex((obj) => obj.uuid === payload.uuid);
    if (index > -1) {
      Vue.set(state.playlists, index, payload);
    } else {
      state.playlists.push(payload);
    }
  },
  SET_MEDIA_APPEARANCES: (state, { uuid, payload }) => {
    Vue.set(state.mediaAppearances, uuid, payload);
  },
};

const actions = {
  loadPlaylist: async (context, { uuid }) => {
    const url = `${LIBRARY_ENDPOINT}playlist/${uuid}/`;
    APIClient.get(url).then((response) => {
      context.commit('SET_PLAYLIST', { payload: response.data });
    }).catch((e) => {
      console.warn('unable to load playlist', e);
    });
  },
  loadMediaAppearances: async (context, { uuid }) => {
    const url = `${LIBRARY_ENDPOINT}media/${uuid}/appearances/`;
    APIClient.get(url).then((response) => {
      context.commit('SET_MEDIA_APPEARANCES', { uuid, payload: response.data });
    }).catch((e) => {
      console.warn('unable to load media appearances', e);
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
