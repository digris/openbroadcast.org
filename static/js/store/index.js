import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import axios from 'axios';

Vue.use(Vuex);

const api_client = axios.create({
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
});

export default new Vuex.Store({
    state: {
        settings: {
            search_exact_match_mode: false
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
            key: 'store'
        })
    ]

});
