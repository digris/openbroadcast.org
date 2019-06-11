import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import schedule from './_schedule';

Vue.use(Vuex);

export default new Vuex.Store({
    namespaced: true,
    modules: {
        schedule,
    },
    state: {
        settings: {
            search_fuzzy_match_mode: false
        },
    },
    mutations: {
        update_settings(state, obj) {
            state.settings[obj.key] = obj.value
        },
    },
    actions: {},
    plugins: [
        createPersistedState({
            key: 'store',
            paths: [
                'settings',
            ]
        })
    ]

});
