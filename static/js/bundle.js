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
import ListFilter from './element/listfilter';

import AutocompleteWidgets from './element/autocomplete-widget';

$(() => {

    const s = new Vue({
        el: '#search_app_ng',
        render: h => h(SearchApp, {
            props: {
                search_scope: 'bar'
            }
        })
    });

    const f = new ListFilter({});
    const _acw = new AutocompleteWidgets({debug: true});

});
