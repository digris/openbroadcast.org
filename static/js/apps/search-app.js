import axios from 'axios';
import debounce from 'debounce';
import ClickOutside from 'vue-click-outside';
import store from '../store';

const api_client = axios.create({
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
});

export default {
  name: 'SearchApp',
  // props: [
  //     'search_scope'
  // ],
  data() {
    return {
      loading: false,
      active: false,
      search_input_has_focus: false,
      search_query_string: '',
      search_query: null,
      search_total_results: 0,
      search_results: [],
      selected_search_result: -1,
      search_display_box: {
        left: 0,
        width: 100,
      },

      //
      search_scope: '_all',
      search_scopes: [
        {
          ct: '_all',
          name: 'All',
          shortcut: '_',
        },
        {
          ct: 'alibrary.artist',
          name: 'Artist',
          shortcut: 'a',
          list_url: '/content/library/artists/',
        },
        {
          ct: 'alibrary.release',
          name: 'Release',
          shortcut: 'r',
          list_url: '/content/library/releases/',
        },
        {
          ct: 'alibrary.media',
          name: 'Track',
          shortcut: 't',
          list_url: '/content/library/tracks/',
        },
        {
          ct: 'alibrary.label',
          name: 'Label',
          shortcut: 'l',
          list_url: '/content/library/labels/',
        },
        {
          ct: 'alibrary.playlist',
          name: 'Playlist',
          shortcut: 'p',
          list_url: '/content/playlists/',
        },
        {
          ct: 'profiles.profile',
          name: 'User',
          shortcut: 'u',
          list_url: '/network/users/',
        },
      ],
    };
  },
  created() {
    const scope = $('body').data('scope');

    if (scope !== undefined && scope !== '') {
      this.search_scope = scope;
    }
  },
  mounted() {

  },
  directives: {
    ClickOutside,
  },
  computed: {
    settings: () => store.state.settings,
    result_is_visible() {
      return this.search_results.length > 0;
    },
  },
  methods: {

    // store methods
    // update_settings: (key, value) => store.commit('update_settings', {key: key, value: value}),

    update_settings(key, value) {
      store.commit('update_settings', { key, value });

      // query needs to be refreshed if mode changes
      if (key === 'search_fuzzy_match_mode') {
        this.load_search_results();
      }
    },
    // /////////////////////////////////////////////////////////////
    // component activation / deactivation
    // /////////////////////////////////////////////////////////////
    activate_search(e) {
      // TODO: improve size/position handling
      this.search_display_box.left = $('.controls.search-input').position().left;
      this.search_display_box.width = $('.controls.search-input').width();

      this.active = true;
    },
    deactivate_search(e) {
      this.search_results = [];
      this.search_query_string = '';
      this.active = false;
    },

    // /////////////////////////////////////////////////////////////
    // input field handling
    // /////////////////////////////////////////////////////////////
    update_query_string(e) {
      const q = e.target.value;
      console.debug(q);

      this.search_query_string = q;

      if (q.length > 1) {
        // this.search_results = dummy_results;
        this.parse_query_string(q);
        this.load_search_results({ q });
      } else {
        this.search_results = [];
      }
    },
    search_input_focus() {
      this.activate_search();
      this.search_input_has_focus = true;
    },
    search_input_blur() {
      this.search_input_has_focus = false;
    },
    search_input_esc: debounce(function (e) {
      // this.deactivate_search();
      this.search_query_string = '';
      this.search_results = [];
    }, 100),

    // /////////////////////////////////////////////////////////////
    // result selection & navigation
    // /////////////////////////////////////////////////////////////
    select_search_result(e, offset) {
      e.stopPropagation();
      if (offset) {
        this.selected_search_result += offset;

        if (this.selected_search_result < -1) {
          this.selected_search_result = -1;
        }
        if (this.selected_search_result >= this.search_results.length) {
          this.selected_search_result = this.search_results.length - 1;
        }
      } else {
        this.selected_search_result = -1;
      }

      $.each(this.search_results, (i, el) => {
        el.selected = i === this.selected_search_result;
      });
    },
    // result navigation
    navigate_to_selection(e) {
      let item = null;

      if (this.search_results.length === 1) {
        item = this.search_results[0];
      } else {
        item = this.search_results[this.selected_search_result];
      }


      if (item !== undefined) {
        this.search_results = [];
        this.search_query_string = '';
        document.location.href = item.url;

        // Turbolinks.visit(item.detail_url);
      } else {
        // alert(this.search_query_string);
        const scope = this.search_scopes.find((scope) => scope.ct === this.search_scope);

        if (scope.list_url === undefined) {
          return;
        }

        let q = this.search_query_string;
        if (q[1] === ':') {
          q = $.trim(q.substr(2));
        }

        const params = {
          search_q: q,
          option_fuzzy: (this.settings.search_fuzzy_match_mode ? 1 : 0),
        };

        document.location.href = `${scope.list_url}?${$.param(params)}`;
      }
    },
    // result navigation
    navigate_to_item(e, item) {
      document.location.href = item.url;
    },

    // /////////////////////////////////////////////////////////////
    // parse query string
    // /////////////////////////////////////////////////////////////
    parse_query_string(q) {
      if (q && q.length >= 2 && q[1] === ':') {
        const shortcut = q[0];

        const scope = this.search_scopes.find((scope) => scope.shortcut === shortcut);
        this.set_search_scope(scope.ct);

        console.log('shortcut detected:', shortcut, scope);
      }
    },

    // /////////////////////////////////////////////////////////////
    // settings / scope
    // /////////////////////////////////////////////////////////////
    set_search_scope(scope) {
      if (scope) {
        this.search_scope = scope;
      } else {
        this.search_scope = null;
      }
      this.load_search_results();
    },


    // /////////////////////////////////////////////////////////////
    // data handling / ajax loading
    // /////////////////////////////////////////////////////////////
    // load_search_results: function (query = false) {
    //
    //     if (!query) {
    //         query = {
    //             q: this.search_query_string
    //         }
    //     }
    //     if (query.q.length < 1) {
    //         this.search_results = [];
    //         this.search_total_results = 0;
    //         return
    //     }
    //
    //     // add search options
    //     query['fuzzy'] = (this.settings.search_fuzzy_match_mode ? 1 : 0);
    //     query['ct'] = this.search_scope;
    //
    //
    //     console.debug('query', query);
    //     this.loading = true;
    //
    //     // "http://api.icndb.com/jokes/random/10"
    //     let url = '/api/v2/search/global/';
    //
    //     api_client.get(url, {params: query})
    //         .then((response) => {
    //             this.loading = false;
    //
    //             let max_score = response.data.max_score;
    //
    //             // TODO: make this less ugly...
    //             $.each(response.data.results, (i, el) => {
    //                 el.selected = false;
    //                 //el.score = el.score / max_score;
    //                 el.top_hit = el.score > 8;
    //                 //el.top_hit = (el.score / max_score) > 0.7;
    //                 el.scope = this.search_scopes.find((scope) => {
    //                     return scope.ct === el.ct
    //                 });
    //             });
    //
    //             this.search_total_results = response.data.total;
    //             this.search_results = response.data.results;
    //
    //         }, (error) => {
    //             this.loading = false;
    //         })
    // },


    // /////////////////////////////////////////////////////////////
    // data handling / ajax loading
    // /////////////////////////////////////////////////////////////
    load_search_results: debounce(function (query = false) {
      if (!query) {
        query = {
          q: this.search_query_string,
        };
      }
      if (query.q.length < 1) {
        this.search_results = [];
        this.search_total_results = 0;
        return;
      }

      // add search options
      query.fuzzy = (this.settings.search_fuzzy_match_mode ? 1 : 0);
      query.ct = this.search_scope;


      console.debug('query', query);
      this.loading = true;

      // "http://api.icndb.com/jokes/random/10"
      const url = '/api/v2/search/global/';

      api_client.get(url, { params: query })
        .then((response) => {
          this.loading = false;

          const { max_score } = response.data;

          // TODO: make this less ugly...
          $.each(response.data.results, (i, el) => {
            el.selected = false;
            // el.score = el.score / max_score;
            el.top_hit = el.score > 8;
            // el.top_hit = (el.score / max_score) > 0.7;
            el.scope = this.search_scopes.find((scope) => scope.ct === el.ct);
          });

          this.search_total_results = response.data.total;
          this.search_results = response.data.results;
        }, (error) => {
          this.loading = false;
        });
    }, 350),

  },
};
