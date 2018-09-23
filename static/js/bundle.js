// legacy stylesheet imports
import '../sass/screen.sass'
//import '../sass/print.sass'
import '../sass/aplayer.sass'
import '../sass/scheduler.sass'
//import '../sass/admin.sass'

// global stylesheet import
import '../sass/bundle.sass';

import Vue from 'vue';
import Vuex from 'vuex';

const DEBUG = true;

Vue.use(Vuex);

import SearchApp from './apps/search-app.vue';
import PlayerApp from './apps/player/player-app.vue';
import Topbar from './element/topbar';
import ListFilter from './element/listfilter';

import AutocompleteWidgets from './element/autocomplete-widget';

$(() => {

    /******************************************************************
     * TODO: move initializers to appropriate place
     ******************************************************************/
    const search_app_selector = $('#search_app_home').length ? "search_app_home" : "search_app";
    const search_app_el = document.getElementById(search_app_selector);
    if(search_app_el) {
        if (DEBUG) console.debug('initialize SearchApp:', search_app_el);
        const _SearchApp = new Vue({
            el: search_app_el,
            render: h => h(SearchApp, {
                props: {
                    search_scope: 'bar'
                }
            })
        });
    }

    // const player_app_el = document.getElementById('player_app');
    // if(player_app_el) {
    //     if (DEBUG) console.debug('initialize PlayerApp:', player_app_el);
    //     const _PlayerApp = new Vue({
    //         el: player_app_el,
    //         render: h => h(PlayerApp)
    //     })
    // }


    const _Topbar = new Topbar();
    const _ListFilter = new ListFilter();
    const _AutocompleteWidgets= new AutocompleteWidgets();

    if (DEBUG) console.info('jquery bundle:', $.fn.jquery)

});
