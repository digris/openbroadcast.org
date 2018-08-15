;

// legacy stylesheet imports
import '../sass/screen.sass'
//import '../sass/print.sass'
import '../sass/aplayer.sass'
import '../sass/scheduler.sass'
//import '../sass/admin.sass'

// global stylesheet import
import '../sass/bundle.sass';


//
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import SearchApp from './apps/search-app.vue';
import Topbar from './element/topbar';
import ListFilter from './element/listfilter';

import AutocompleteWidgets from './element/autocomplete-widget';

$(() => {

    // TODO: move to appropriate place
    //const search_app_selector = '#search_app';
    const search_app_selector = $('#search_app_home').length ? "#search_app_home" : "#search_app";
    const s = new Vue({
        el: search_app_selector,
        render: h => h(SearchApp, {
            props: {
                search_scope: 'bar'
            }
        })
    });

    const t = new Topbar();
    const f = new ListFilter({});
    const _acw = new AutocompleteWidgets({debug: true});

});
