/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';
// eslint-disable-next-line import/no-cycle
import store from './index';
// eslint-disable-next-line import/no-cycle
import { addNotification } from '../components/Notifications/utils';

const EXPORT_ENDPOINT = '/api/v2/exporter/export/';

const state = {
  exports: [],
};

const getters = {
  exports: (state) => state.exports,
};

const mutations = {
  setExport: (state, { payload }) => {
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
      });
    }).catch((e) => {
      console.warn('unable to load exports', e);
    });
  },
  createExport: async (context, { objectKeys }) => {
    const url = EXPORT_ENDPOINT;
    const payload = {
      objects: objectKeys,
    };
    APIClient.post(url, payload).then(() => {
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


// event listeners (currently used in legacy / non-vuejs context)
window.addEventListener('exporter:exportObjects', (e) => {
  const objectKeys = e.detail;
  store.dispatch('exporter/createExport', { objectKeys });
});
