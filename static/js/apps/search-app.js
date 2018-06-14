import store from "../store";
import axios from 'axios';
import debounce from 'debounce';

const api_client = axios.create({
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
});


let dummy_results = [
    {
        name: 'foo',
        selected: false,
    },
    {
        name: 'bar',
        selected: false,
    },
];

export default {
    name: 'SearchApp',
    // props: [
    //     'search_scope'
    // ],
    data() {
        return {
            loading: false,
            search_input_has_focus: false,
            search_query_string: '',
            search_query: null,
            search_total_results: null,
            search_results: [],
            selected_search_result: -1,

            //
            search_scope: null
        }
    },
    mounted () {
    },
    computed: {
        settings: () => store.state.settings,
        result_is_visible: function () {
            return this.search_results.length > 0;
        }
    },
    methods: {

        // store methods
        //update_settings: (key, value) => store.commit('update_settings', {key: key, value: value}),

        update_settings: function(key, value) {

            store.commit('update_settings', {key: key, value: value})

            // query needs to be refreshed if mode changes
            if(key === 'search_exact_match_mode') {
                this.load_search_results();
            }

        },


        ///////////////////////////////////////////////////////////////
        // input field handling
        ///////////////////////////////////////////////////////////////
        update_query_string: function (e) {
            let q = e.target.value;
            console.debug(q);

            this.search_query_string = q;

            if (q.length > 0) {
                //this.search_results = dummy_results;
                this.load_search_results({q: q});
            } else {
                this.search_results = [];
            }

        },
        search_input_focus: function () {
            this.search_input_has_focus = true;
        },
        search_input_blur: function () {
            this.search_input_has_focus = false;
        },
        search_input_esc: debounce(function (e) {
            this.search_query_string = '';
            this.search_results = [];
        }, 100),

        ///////////////////////////////////////////////////////////////
        // result selection & navigation
        ///////////////////////////////////////////////////////////////
        select_search_result: function (e, offset) {
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
        navigate_to_selected_search_result: function (e) {

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

                //Turbolinks.visit(item.detail_url);
            }

        },

        ///////////////////////////////////////////////////////////////
        // settings / scope
        ///////////////////////////////////////////////////////////////
        set_search_scope: function (scope) {
            if (scope) {
                this.search_scope = scope;
            } else {
                this.search_scope = null;
            }
        },


        ///////////////////////////////////////////////////////////////
        // data handling / ajax loading
        ///////////////////////////////////////////////////////////////
        load_search_results: function (query = false) {

            if(! query) {
                query = {
                    q: this.search_query_string
                }
            }
            console.debug('query', query);

            if(query.q.length < 1) {
                this.search_results = [];
                this.search_total_results = null;
                return
            }

            // add settings
            //query['exact_match'] = this.settings.search_exact_match_mode;
            query['exact'] = (this.settings.search_exact_match_mode ? 1 : 0);


            console.debug('query', query);
            this.loading = true;

            // "http://api.icndb.com/jokes/random/10"
            let url = '/api/v2/search/global/';

            api_client.get(url, {params: query})
                .then((response) => {
                    this.loading = false;

                    // TODO: make this less ugly...
                    $.each(response.data.results, (i, el) => {
                        el.selected = false;
                    });

                    this.search_total_results = response.data.total;
                    this.search_results = response.data.results;

                }, (error) => {
                    this.loading = false;
                })
        },

    }
}
