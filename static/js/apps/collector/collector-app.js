import Vue from 'vue';
import APIClient from '../../api/client';
import debounce from 'debounce';
import Modal from '../../components/modal.vue';
import Playlist from './components/playlist.vue'
import {template_filters} from '../../utils/template-filters';

const DEBUG = true;

const CollectorApp = Vue.extend({
    components: {
        Modal,
        Playlist
    },
    data() {
        return {
            loading: false,
            scope: 'list',
            show_modal: false,
            items_to_collect: null,
            query_string: '',
            playlists: [],

            new_playlist_name: ''
        }
    },
    mounted: function () {
        if (DEBUG) console.group('CollectorApp');

        // load last used query string
        this.query_string = localStorage.getItem('collector.query_string') || '';

        window.addEventListener('collector:collect', (e) => {
            if (DEBUG) console.info('collector:collect', e.detail);
            this.items_to_collect = e.detail;
            this.show_modal = true;
            this.load_playlists();
        }, false);

        if (DEBUG) console.groupEnd();
    },
    filters: template_filters,
    computed: {},
    methods: {
        set_scope: function (scope) {
            this.scope = scope;
        },
        update_query_string: function (e) {
            const q = e.target.value;
            this.query_string = q;
            localStorage.setItem('collector.query_string', q);
            this.load_playlists();
        },
        load_playlists: debounce(function () {

            const url = '/api/v2/collector/playlist/';
            const payload = {
                q: this.query_string,
                fields: ['url', 'uuid', 'name', 'series_display', 'num_media', 'duration', 'image'].join(',')
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
        add_item_to_playlist: function (playlist) {
            if (DEBUG) console.info('add_item_to_playlist', playlist.name);
            this.add_items_to_playlist(playlist, this.items_to_collect);
        },
        // method for API communication
        add_items_to_playlist: function (playlist, items_to_collect) {
            if (DEBUG) console.info('add_items_to_playlist', playlist.name, items_to_collect);

            const index = this.playlists.findIndex((element) => element.uuid === playlist.uuid);

            playlist.num_media = playlist.num_media + 1;
            playlist.loading = true;
            playlist.updated = false;


            APIClient.put(playlist.url, {items_to_collect: items_to_collect})
                .then((response) => {
                    if (index > -1) {
                        this.$set(this.playlists, index, response.data)
                        response.data.updated = true;
                    }
                }, (error) => {
                    console.error('error putting data', error);
                    playlist.loading = true;
                });
        },

        update_new_playlist_name: function (e) {
            this.new_playlist_name = e.target.value;
        },
        create_playlist: function () {
            const name = this.new_playlist_name;

            const url = '/api/v2/library/playlist/';
            const payload = {
                name: name,
            };

            APIClient.post(url, payload)
                .then((response) => {
                    console.log(response.data);

                    //this.add_items_to_playlist(response.data, this.items_to_collect);


                    this.scope = 'list';
                    this.query_string = '';
                    this.load_playlists();


                }, (error) => {
                    console.error('error posting data', error);
                    playlist.loading = true;
                });

        },

        close: function () {
            this.show_modal = false;
        }
    }
});

module.exports = CollectorApp;
