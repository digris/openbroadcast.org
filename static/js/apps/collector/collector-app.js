import Vue from 'vue';
import APIClient from '../../api/client';
import debounce from 'debounce';
import Modal from '../../components/ui/Modal.vue';
import Visual from '../../components/ui/Visual.vue';
import Loader from '../../components/ui/Loader.vue';
import Playlist from './components/playlist.vue'
import {templateFilters} from '../../utils/template-filters';
import {visit_by_resource} from '../../utils/visit-by-resource';

const DEBUG = true;

const CollectorApp = Vue.extend({
    components: {
        Modal,
        Loader,
        Playlist,
        Visual
    },
    data() {
        return {
            loading: false,
            scope: 'list',
            show_modal: false,
            items_to_collect: null,
            query_string: '',
            playlists: [],

            create_playlist_data: {
                name: '',
                type: 'playlist',
                errors: [],
                created: null
            }
        }
    },
    mounted: function () {
        if (DEBUG) console.group('CollectorApp');

        // load last used query string
        this.query_string = localStorage.getItem('collector.query_string') || '';

        window.addEventListener('collector:collect', (e) => {
            if (DEBUG) console.info('collector:collect', e.detail);
            this.items_to_collect = e.detail;
            this.scope = 'list';
            this.show_modal = true;
            this.load_playlists();
        }, false);

        if (DEBUG) console.groupEnd();
    },
    filters: templateFilters,
    computed: {},
    methods: {

        ///////////////////////////////////////////////////////////////
        // generic
        ///////////////////////////////////////////////////////////////
        close: function () {
            this.show_modal = false;
        },

        ///////////////////////////////////////////////////////////////
        // add to playlist
        ///////////////////////////////////////////////////////////////
        set_scope_list: function () {
            this.scope = 'list';
        },
        update_query_string: function (e) {
            const q = e.target.value;
            this.query_string = q;
            localStorage.setItem('collector.query_string', q);
            this.load_playlists();
        },
        load_playlists: debounce(function () {

            //const url = '/api/v2/collector/playlist/';
            const url = '/api/v2/library/playlist/collect/';
            const payload = {
                q: this.query_string,
                limit: 20,
                fields: ['url', 'uuid', 'name', 'item_appearances', 'series_display', 'num_media', 'duration', 'image'].join(',')
            };

            $.ajax(url, {
                dataType: 'json',
                data: payload
            }).then((data) => {
                if (DEBUG) console.debug('data from api:', data);
                this.playlists = data.results;
            });
        }, 200),
        // method called from ui
        add_item_to_playlist: function (playlist, close) {
            if (DEBUG) console.info('add_item_to_playlist', playlist.name, close);
            this.add_items_to_playlist(playlist, this.items_to_collect);
            if(close) {
                this.close()
            }
        },
        // method for API communication
        add_items_to_playlist: function (playlist, items_to_collect) {
            if (DEBUG) console.info('add_items_to_playlist', playlist.name, items_to_collect);

            const index = this.playlists.findIndex((element) => element.uuid === playlist.uuid);

            playlist.num_media = playlist.num_media + 1;
            playlist.loading = true;

            APIClient.put(playlist.url, {items_to_collect: items_to_collect})
                .then((response) => {
                    if (index > -1) {
                        this.$set(this.playlists, index, response.data)
                    }
                }, (error) => {
                    console.error('error putting data', error);
                    playlist.loading = false;
                });
        },

        ///////////////////////////////////////////////////////////////
        // playlist create
        ///////////////////////////////////////////////////////////////
        set_scope_create: function () {
            this.scope = 'create';

            let initial = {
                name: '',
                type: this.create_playlist_data.type,
                errors: [],
                created: null
            };

            this.create_playlist_data = initial;

            setTimeout(() => {
                this.$refs.playlist_create_name.focus();
            }, 1)

        },
        create_playlist: function () {

            let data = this.create_playlist_data;

            // validate
            data.errors = [];

            if (!data.name) {
                data.errors.push("Name required.");
            }

            if (data.errors.length > 0) {
                console.warn('form errors:', data.errors);
                return;
            }


            const url = '/api/v2/library/playlist/';
            const payload = {
                name: data.name,
                type: data.type,
                items_to_collect: this.items_to_collect
            };

            this.loading = true;

            /**/
            APIClient.post(url, payload)
                .then((response) => {
                    console.log(response.data);

                    this.create_playlist_data = {
                        name: '',
                        type: this.create_playlist_data.type,
                        errors: [],
                        created: response.data
                    };
                    this.loading = false;
                    this.load_playlists();
                }, (error) => {
                    console.error('error posting data', error);
                    this.loading = false;
                });


        },
        visit: visit_by_resource,
    }
});

module.exports = CollectorApp;
