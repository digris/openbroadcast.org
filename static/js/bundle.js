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


$(function () {
    let s = new Vue({
        el: '#search_app_ng',
        render: h => h(SearchApp, {
            props: {
                search_scope: 'bar'
            }
        })
    });

});
