/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';


const DEBUG = false;


const generateKey = function (ct, uuid) {
  return `${ct}:${uuid}`;
};

const state = {
  selection: [],
};

const getters = {
  selection: (state) => state.selection,
  numSelected: (state) => state.selection.length,
  objectSelection: (state) => (ct, uuid) => {
    const key = generateKey(ct, uuid);
    return state.selection.indexOf(key) > -1;
  },
};

const mutations = {
  addToSelection: (state, { key }) => {
    if (DEBUG) console.debug('mutations - addToSelection', key);
    state.selection.push(key);
  },
  removeFromSelection: (state, { key }) => {
    if (DEBUG) console.debug('mutations - removeFromSelection', key);
    const index = state.selection.indexOf(key);
    if (index > -1) {
      state.selection.splice(index, 1);
    }
  },
};

const actions = {
  // eslint-disable-next-line no-shadow
  toggleSelection: ({ commit, getters }, { ct, uuid }) => {
    const key = generateKey(ct, uuid);
    if(getters.selection.indexOf(key) < 0) {
      commit('addToSelection', { key });
    } else {
      commit('removeFromSelection', { key });
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
