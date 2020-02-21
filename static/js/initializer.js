/** ********************************************************************
 * AppInitializer handles setup (re-)initialization of
 * our mixed app stack. Some apps are global (like search) others
 * 'local' - like chat.
 * so chat has only to be initialized in chat context.
 * further we need to re-initialize apps on document reload -
 * e.g. form POST
 *
 * setup cacle has to run on both document.ready and XHR based
 * navigation via turbolinks
 ********************************************************************* */

import Vue from 'vue';
import Vuex from 'vuex';
import settings from './settings';
import store from './store/index';
import SearchApp from './apps/search-app.vue';
import PlayerApp from './apps/player/player-app.vue';
import PlayerControlApp from './apps/player/player-control-app.vue';
import CollectorApp from './apps/collector/collector-app.vue';
import Topbar from './element/topbar';
import Tagcloud from './element/tagcloud';
import ListFilter from './element/listfilter';
import AutocompleteWidgets from './element/autocomplete-widget';
import LayzImageLoader from './utils/lazy-image-loader';

//
import Player from './components/Player/Player.vue';
import Scheduler from './components/scheduler/Scheduler.vue';
import PlaylistEditor from './components/PlaylistEditor/PlaylistEditor.vue';
//
import ThumbRating from './components/rating/ThumbRating.vue';
import ObjectActions from './components/ObjectActions/ObjectActions.vue';
import EmissionHistory from './components/EmissionHistory/EmissionHistory.vue';
import Visual from './components/ui/Visual.vue';
import LazyImage from './components/ui/LazyImage.vue';
import VisualWithActions from './components/ui/VisualWithActions.vue';
// forms
import Formset from './components/form/Formset.vue';
import InputContainer from './components/form/InputContainer.vue';
import TagInputContainer from './components/form/TagInputContainer.vue';
import APIClient from './api/caseTranslatingClient';

const DEBUG = false;

class AppInitializer {
  constructor(opts) {
    if (DEBUG) console.debug('AppInitializer - constructor');

    // initialize vue root app
    new Vue({
      el: '#app',
      store,
      components: {
        // generic ui components
        visual: Visual,
        'lazy-image': LazyImage,
        'visual-with-actions': VisualWithActions,
        // form ui components
        formset: Formset,
        'input-container': InputContainer,
        'tag-input-container': TagInputContainer,
        //
        scheduler: Scheduler,
        player: Player,
        'playlist-editor': PlaylistEditor,
        'thumb-rating': ThumbRating,
        'object-actions': ObjectActions,
        'emission-history': EmissionHistory,
      },
      mounted() {
        // tell jQuery (legacy) to continue
        if (window.jQuery) {
          window.jQuery.holdReady(false);
        }
      },
    });

    this.apps = [];
    this.bindings();
    this.setup_apps();
  }

  bindings() {

  }

  setup_apps() {
    if (DEBUG) console.debug('AppInitializer - setup_apps');

    const search_app_selector = $('#search_app_home').length ? 'search_app_home' : 'search_app';
    const search_app_el = document.getElementById(search_app_selector);
    if (search_app_el) {
      if (DEBUG) console.debug('initialize SearchApp:', search_app_el);
      const _SearchApp = new Vue({
        el: search_app_el,
        render: (h) => h(SearchApp, {
          props: {
            search_scope: 'bar',
          },
        }),
      });
    }

    const player_app_el = document.getElementById('player_app');
    if (player_app_el) {
      if (DEBUG) console.debug('initialize PlayerApp:', player_app_el);
      const _PlayerApp = new Vue({
        el: player_app_el,
        render: (h) => h(PlayerApp),
      });
    }

    const player_control_app_el = document.getElementById('player_control_app');
    if (player_control_app_el) {
      if (DEBUG) console.debug('initialize PlayerControlApp:', player_control_app_el);
      const _PlayerControlApp = new Vue({
        el: player_control_app_el,
        render: (h) => h(PlayerControlApp),
      });
    }

    const collector_app_el = document.getElementById('collector_app');
    if (collector_app_el) {
      if (DEBUG) console.debug('initialize CollectorApp:', collector_app_el);
      const _CollectorApp = new Vue({
        el: collector_app_el,
        render: (h) => h(CollectorApp),
      });
    }

    const _Topbar = new Topbar();
    const _Tagcloud = new Tagcloud();
    const _ListFilter = new ListFilter();
    const _AutocompleteWidgets = new AutocompleteWidgets();
    const _LayzImageLoader = new LayzImageLoader();
  }
}

export default AppInitializer;
