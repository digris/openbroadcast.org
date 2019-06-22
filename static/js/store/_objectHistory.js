/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';

const DEBUG = true;
const HISTORY_ENDPOINT = '/api/v2/abcast/history-for-object/';

const generateKey = function(objCt, objUuid) {
    return `${objCt}:${objUuid}`;
};

const state = {
    objectHistory: {},
};

const getters = {
    objectHistory: state => state.objectHistory,
    // objectHistoryByKey: (state) => (key) => {
    //     return state.objectHistory.find(obj => todo.obj === obj);
    // }
    objectHistoryByKey: (state) => (objCt, objUuid) => {
        const key = generateKey(objCt, objUuid);
        console.log('objectHistoryByKey', key);
        return state.objectHistory[key] || null;
    }
};

const mutations = {
    setObjectHistory: (state, {key, payload}) => {
        if (DEBUG) console.debug('mutations - setObjectHistory', key, payload);
        Vue.set(state.objectHistory, key, payload);

    },
};

const actions = {
    loadObjectHistory: async (context, {objCt, objUuid}) => {
        const key = generateKey(objCt, objUuid);
        const url = `${HISTORY_ENDPOINT}${key}`;
        context.commit('setObjectHistory', {key: key, payload: []});
        if (DEBUG) console.debug('actions - loadObjectHistory', url);
        APIClient.get(url).then((response) => {
            context.commit('setObjectHistory', {key: key, payload: response.data});
        }).catch(() => {
            context.commit('setObjectHistory', {key: key, payload: null});
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
