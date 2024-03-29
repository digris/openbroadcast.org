import Vue from 'vue';
// import settings from './settings';
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

// eslint-disable-next-line no-unused-vars
import { ActionHandler } from './utils/actionHandler';

//
import Player from './components/Player/Player.vue';
import Scheduler from './components/Scheduler/Scheduler.vue';
import PlaylistEditor from './components/PlaylistEditor/PlaylistEditor.vue';
import ObjectRating from './components/ObjectRating/ObjectRating.vue';
import ObjectRatingMini from './components/ObjectRating/ObjectRatingMini.vue';
import ObjectActions from './components/ObjectActions/ObjectActions.vue';
import ObjectSingleAction from './components/ObjectActions/ObjectSingleAction.vue';
import ObjectStatistics from './components/ObjectStatistics/ObjectStatistics.vue';
import ListActions from './components/ListActions/ListActions.vue';
import EmissionHistory from './components/EmissionHistory/EmissionHistory.vue';
import EmissionHistoryInline from './components/EmissionHistory/EmissionHistoryInline.vue';
import Exporter from './components/Exporter/Exporter.vue';
import MediaPreflightStatus from './components/MediaPreflightStatus/MediaPreflightStatus.vue';
import ObjectMerge from './components/ObjectMerge/ObjectMerge.vue';
import MediaReassign from './components/MediaReassign/MediaReassign.vue';
import Notifications from './components/Notifications/Notifications.vue';
import TagList from './components/Tags/TagList.vue';
// UI
import Card from './components/UI/Card.vue';
import Visual from './components/UI/Visual.vue';
import LazyImage from './components/UI/LazyImage.vue';
import Lightbox from './components/UI/Lightbox.vue';
import ExpandableList from './components/UI/ExpandableList.vue';
import VisualWithActions from './components/UI/VisualWithActions/VisualWithActions.vue';
import ObjectSelectionAction from './components/UI/ObjectSelectionAction.vue';
// Library
import MediaRow from './components/Library/MediaRow.vue';
import MediaAppearances from './components/Library/MediaAppearances.vue';
// forms
import Formset from './components/Form/Formset.vue';
import InputContainer from './components/Form/InputContainer.vue';
import TagInputContainer from './components/Form/TagInputContainer.vue';
// plugins
import Tooltip from './plugins/tooltip';

Vue.use(Tooltip);

class AppInitializer {
  constructor() {
    // eslint-disable-next-line no-new
    new Vue({
      el: '#app',
      store,
      components: {
        // generic ui components
        card: Card,
        'media-row': MediaRow,
        'media-appearances': MediaAppearances,
        visual: Visual,
        'lazy-image': LazyImage,
        lightbox: Lightbox,
        'expandable-list': ExpandableList,
        'visual-with-actions': VisualWithActions,
        'object-selection-action': ObjectSelectionAction,
        'object-merge': ObjectMerge,
        'media-reassign': MediaReassign,
        notifications: Notifications,
        'tag-list': TagList,
        // form ui components
        formset: Formset,
        'input-container': InputContainer,
        'tag-input-container': TagInputContainer,
        //
        scheduler: Scheduler,
        player: Player,
        'playlist-editor': PlaylistEditor,
        'object-rating': ObjectRating,
        'object-rating-mini': ObjectRatingMini,
        'object-actions': ObjectActions,
        'object-single-action': ObjectSingleAction,
        'object-statistics': ObjectStatistics,
        'list-actions': ListActions,
        'emission-history': EmissionHistory,
        'emission-history-inline': EmissionHistoryInline,
        exporter: Exporter,
        'media-preflight-status': MediaPreflightStatus,
      },
      mounted() {
        // tell jQuery (legacy) to continue
        if (window.jQuery) {
          window.jQuery.holdReady(false);
        }
      },
    });

    this.apps = [];
    this.setupApps();
  }

  // eslint-disable-next-line class-methods-use-this
  setupApps() {
    const search_app_selector = $('#search_app_home').length ? 'search_app_home' : 'search_app';
    const search_app_el = document.getElementById(search_app_selector);
    if (search_app_el) {
      // eslint-disable-next-line no-new
      new Vue({
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
      // eslint-disable-next-line no-new
      new Vue({
        el: player_app_el,
        render: (h) => h(PlayerApp),
      });
    }

    const player_control_app_el = document.getElementById('player_control_app');
    if (player_control_app_el) {
      // eslint-disable-next-line no-new
      new Vue({
        el: player_control_app_el,
        render: (h) => h(PlayerControlApp),
      });
    }

    const collector_app_el = document.getElementById('collector_app');
    if (collector_app_el) {
      // eslint-disable-next-line no-new
      new Vue({
        el: collector_app_el,
        render: (h) => h(CollectorApp),
      });
    }

    // eslint-disable-next-line no-new
    new Topbar();
    // eslint-disable-next-line no-new
    new Tagcloud();
    // eslint-disable-next-line no-new
    new ListFilter();
    // eslint-disable-next-line no-new
    new AutocompleteWidgets();
    // eslint-disable-next-line no-new
    new LayzImageLoader();
  }
}

export default AppInitializer;
