/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import dayjs from 'dayjs';
import Vue from 'vue';
// import APIClient from '../api/caseTranslatingClient';

import APIClient from "../api/caseTranslatingClient";

const DEBUG = true;
const DEFAULT_SCHEDULER_CONFIG = {
    numDays: 7,
    daysOffset: 0,
    pixelHeightPerHour: 48,
    snapMinutes: 15,
    emissionColor: 0,
};
// const EMISSION_ENDPOINT = '/api/v2/abcast/emission/?limit=400&time_start_0=2019-06-03+06%3A00&time_start_1=2019-06-04+06%3A00&fields=uuid,co,name';
const EMISSION_ENDPOINT = '/api/v2/abcast/emission/';
const DEFAULT_EMISSION_FIELDS = [
    'ct',
    'uuid',
    'url',
    'co',
    'name',
    'series',
    'image',
    'time_start',
    'time_end',
    'duration',
    'updated',
    'color',
    'has_lock',
    'co.ct',
    'co.uuid',
    'co.name',
    'co.url',
    'co.duration'
];

const state = {
    settings: null,
    emissions: {},
    clipboard: []
};

const getters = {
    settings: state => state.settings || DEFAULT_SCHEDULER_CONFIG,
    emissions: state => state.emissions,
    clipboard: state => state.clipboard,
    emissionByUuid: (state) => (uuid) => {
        return state.emissions[uuid] || null;
    }
};

const mutations = {
    setSettings: (state, payload) => {
        if (DEBUG) console.debug('mutations - setSettings', payload);
        state.settings = payload;
    },
    setEmission: (state, {uuid, payload, forceUpdate=false}) => {
        // if (DEBUG) console.debug('mutations - setEmission', uuid, payload);

        // TODO: check for a better way.
        // we parse time with dayjs here to only have to do this once
        payload.timeStartObj = dayjs(payload.timeStart);
        // check if exists
        if (state.emissions[uuid] === undefined) {
            Vue.set(state.emissions, uuid, payload);
        } else if (state.emissions[uuid].updated != payload.updated || forceUpdate) {
            if (DEBUG) console.debug('updated', payload.updated);
            Vue.set(state.emissions, uuid, payload);
        }
    },
    removeEmission: (state, {uuid}) => {
        if (DEBUG) console.debug('mutations - removeEmission', uuid);
        Vue.delete(state.emissions, uuid);
    },
    addToClipboard: (state, payload) => {
        if (DEBUG) console.debug('mutations - addToClipboard', payload);

        const index = state.clipboard.findIndex((item) => item.uuid === payload.uuid);
        if (index < 0) {
            state.clipboard.unshift(payload);
        } else {
            Vue.set(state.clipboard, index, payload);
        }
    },
    removeFromClipboard: (state, uuid) => {
        if (DEBUG) console.debug('mutations - removeFromClipboard', uuid);

        const index = state.clipboard.findIndex((item) => item.uuid === uuid);
        if (index > -1) {
            Vue.delete(state.clipboard, index);
        }
    },
    clearClipboard: (state) => {
        if (DEBUG) console.debug('mutations - clearClipboard');
        state.clipboard = [];
    }
};

const actions = {
    setSettings: (context, payload) => {
        context.commit('setSettings', payload);
    },
    setDefaultSettings: (context) => {
        context.commit('setSettings', DEFAULT_SCHEDULER_CONFIG);
    },
    // scheduling
    loadSchedule: async (context, {timeStart, timeEnd, url}) => {
        // eslint-disable-next-line no-param-reassign
        url = url || EMISSION_ENDPOINT;
        const params = {
            limit: 500,
            fields: DEFAULT_EMISSION_FIELDS.join(','),
            'time_start_0': timeStart,
            'time_start_1': timeEnd,
        };

        if (DEBUG) console.debug('actions - loadSchedule', url, params);
        APIClient.get(url, {params: params}).then((response) => {
            for (let obj of response.data.results) {
                context.commit('setEmission', {uuid: obj.uuid, payload: obj});
            }
            // if(response.data.next !== null) {
            //     console.debug('next:', response.data.next);
            //     const next = response.data.next;
            //     context.dispatch('loadSchedule', {timeStart, timeEnd, next});
            // }
        }).catch(() => {
            console.warn('error');
        });
    },
    loadEmission: async (context, uuid) => {
        if (DEBUG) console.debug('actions - loadEmission', uuid);
        const url = `${EMISSION_ENDPOINT}${uuid}/`;
        const response = await APIClient.get(url);
        const obj = response.data;
        context.commit('setEmission', {uuid: obj.uuid, payload: obj, forceUpdate: true});
        return response;
    },
    createEmission: async (context, {contentObj, timeStart, color}) => {
        if (DEBUG) console.debug('actions - createEmission', contentObj, timeStart, color);
        const url = EMISSION_ENDPOINT;
        const payload = {
            'obj_ct': contentObj.ct,
            'obj_uuid': contentObj.uuid,
            'time_start': timeStart,
            'color': color,
        };
        const response = await APIClient.post(url, payload);
        const obj = response.data;
        context.commit('setEmission', {uuid: obj.uuid, payload: obj});
        return response;
    },
    updateEmission: async (context, {emission, payload}) => {
        if (DEBUG) console.debug('actions - updateEmission', emission, payload);
        // const payload = {
        //     'time_start': timeStart,
        // };
        const response = await APIClient.patch(emission.url, payload);
        const obj = response.data;
        context.commit('setEmission', {uuid: obj.uuid, payload: obj});
        return response;
    },
    deleteEmission: async (context, uuid) => {
        if (DEBUG) console.debug('actions - deleteEmission', uuid);
        const url = `${EMISSION_ENDPOINT}${uuid}/`;
        const response = await APIClient.delete(url);
        context.commit('removeEmission', {uuid: uuid});
        return response;
    },
    // clipboard handling
    addToClipboard: async (context, payload) => {
        if (DEBUG) console.debug('actions - addToClipboard', payload);
        context.commit('addToClipboard', payload);
        APIClient.get(payload.url).then((response) => {
            context.commit('addToClipboard', response.data);
        }).catch(() => {
            console.warn('error');
        });
    },
    removeFromClipboard: async (context, uuid) => {
        if (DEBUG) console.debug('actions - removeFromClipboard', uuid);
        context.commit('removeFromClipboard', uuid);
    },

    clearClipboard: (context) => {
        if (DEBUG) console.debug('actions - clearClipboard');
        context.commit('clearClipboard');
    },
};

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
};
