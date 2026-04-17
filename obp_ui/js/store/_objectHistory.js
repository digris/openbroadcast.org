/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';

const HISTORY_ENDPOINT = '/api/v2/abcast/history-for-object/';

const generateKey = (objCt, objUuid) => `${objCt}:${objUuid}`;

const state = {
  objectHistory: {},
};

const getters = {
  objectHistory: (state) => state.objectHistory,
  // objectHistoryByKey: (state) => (key) => {
  //     return state.objectHistory.find(obj => todo.obj === obj);
  // }
  objectHistoryByKey: (state) => (objCt, objUuid) => {
    const key = generateKey(objCt, objUuid);
    return state.objectHistory[key] || null;
  },
};

const mutations = {
  setObjectHistory: (state, { key, payload }) => {
    Vue.set(state.objectHistory, key, payload.results);
  },
};

const actions = {
  loadObjectHistory: async (context, { objCt, objUuid }) => {
    const key = generateKey(objCt, objUuid);
    const url = `${HISTORY_ENDPOINT}${key}/`;
    context.commit('setObjectHistory', { key, payload: { count: 0, results: [] } });
    APIClient.get(url).then((response) => {
      context.commit('setObjectHistory', { key, payload: response.data });
    }).catch(() => {
      context.commit('setObjectHistory', { key, payload: null });
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
