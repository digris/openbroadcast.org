/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';
import store from './index';
import {addNotification} from '../components/Notifications/utils';

const DEBUG = true;
const EXPORT_ENDPOINT = '/api/v2/exporter/export/';

const state = {
  exports: [],
};

const getters = {
  exports: (state) => state.exports,
};

const mutations = {
  setExport: (state, { payload }) => {
    if (DEBUG) console.debug('mutations - setExport', payload);

    const index = state.exports.findIndex((obj) => obj.uuid === payload.uuid);
    if (index > -1) {
      Vue.set(state.exports, index, payload);
    } else {
      state.exports.push(payload);
    }
  },
};

const actions = {
  loadExport: async (context, { uuid }) => {
    const url = `${EXPORT_ENDPOINT}${uuid}/`;
    APIClient.get(url).then((response) => {
      context.commit('setExport', { payload: response.data });
    }).catch((e) => {
      console.warn('unable to load export', e);
    });
  },
  loadExports: async (context) => {
    const url = `${EXPORT_ENDPOINT}`;
    APIClient.get(url).then((response) => {
      response.data.results.forEach((obj) => {
        context.commit('setExport', { payload: obj });
      })
    }).catch((e) => {
      console.warn('unable to load exports', e);
    });
  },
  createExport: async (context, { objectKeys }) => {
    if (DEBUG) console.debug('createExport', objectKeys);
    const url = EXPORT_ENDPOINT;
    const payload = {
      objects: objectKeys,
    };
    APIClient.post(url, payload).then((response) => {
      if (DEBUG) console.debug('createExport', response);
      // context.commit('setExport', { payload: response.data });
      addNotification({
        title: 'Download queued',
        body: 'The files are now being processed in the background and will then be added to your <a href="/content/download/">download queue</a>.',
        lifetime: 5000,
      });
    }).catch((e) => {
      console.warn('unable to create export', e);
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


// event listeners
window.addEventListener('exporter:exportObjects', (e) => {
  const objectKeys = e.detail;
  if (DEBUG) console.debug('exportObjects', objectKeys);
  store.dispatch('exporter/createExport', {objectKeys});
});
