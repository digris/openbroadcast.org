/*
 * PLAYLIST SCRIPTS
 * REFACTORIN TO NUNJUCKS!
 */

/* core */

PlaylistUi = function () {

    var self = this;

    this.interval = false;
    this.interval_loops = 0;
    this.interval_duration = 120000;
    // this.interval_duration = false;
    this.api_url = false;
    this.api_url_simple = false; // used for listings as much faster..

    this.inline_dom_id = 'inline_playlist_holder';
    this.inline_dom_element;

    this.current_playlist_id;

    this.current_data;
    this.current_items = new Array;

    this.init = function () {

        console.log('PlaylistUi: init');
        console.log(self.api_url);

        this.inline_dom_element = $('#' + this.inline_dom_id);

        self.iface();
        self.bindings();

        // set interval and run once
        /*
         if(self.interval_duration) {
         self.set_interval(self.run_interval, self.interval_duration);
         }
         self.run_interval();
         */
        self.load();
        /*
         pushy.subscribe(self.api_url + self.current_playlist_id + '/', function() {
         debug.debug('pushy callback');
         self.load();
         });
         */


    };

    this.iface = function () {
        // this.floating_inline('lookup_providers', 120)
    };

    this.bindings = function () {


        //self.inline_dom_element.hide(20000)
        var container = $('#inline_playlist_container');

        // states - open / close
        // main box
        $('.ui-persistent > .header', container).live('click', function (e) {
            e.preventDefault();
            var parent = $(this).parents('.ui-persistent');
            if (!parent.hasClass('expanded')) {
                parent.data('uistate', 'expanded');
            } else {
                parent.data('uistate', 'hidden');
            }
        });
        // sub boxes


        // settings panel / create
        $('.ui-persistent > .form form.create', container).live('submit', function (e) {
            e.preventDefault();
            var name = $('input.name', $(this)).val();
            self.create_playlist(name);
        });

        // actions
        $('.playlist_holder > .header a', container).live('click', function (e) {
            e.preventDefault();

            var id = $(this).parents('.playlist_holder').data('object_id');
            var action = $(this).data('action');

            $.log(action, id);

            if (action == 'delete' && confirm('Sure?')) {
                self.delete_playlist(id);
                conatiner.fadeOut(200)
            }

            //var name = $('input.name', $(this)).val();
            //self.create_playlist(name);
        });


        // Playlist as a whole, edit name
        $('div.playlist_holder .header .action.edit').live('click', function () {
            var edit = $('div.edit', $(this).parent().parent().parent());
            if (edit.css("display") == "none") {
                edit.show();
            } else {
                edit.hide();
            }
            return false;
        });

        // Action on name change & Enter
        $('div.playlist_holder .panel .edit input').live('keypress', function (e) {

            if (e.keyCode == 13 || e.keyCode == 9) {
                e.preventDefault();

                var id = $(this).attr('id').split("_").pop();
                ;
                var name = $(this).val();

                // Request data
                var data = {
                    name: name
                };

                $.ajax({
                    url: self.api_url + id + '/',
                    type: 'PUT',
                    data: JSON.stringify(data),
                    dataType: "json",
                    contentType: "application/json",
                    processData: false,
                    success: function (data) {
                        //$('#playlist_holder_' + id).hide(500);
                        self.run_interval();
                    },
                    async: true
                });

            }

        });


        // list items
        $('.action.download > a', self.inline_dom_element).live('click', function (e) {
            e.preventDefault();
        });


        // list-inner items
        $('.list.item a', self.inline_dom_element).live('click', function (e) {

            e.preventDefault();
            var container = $(this).parents('.list.item');
            var action = $(this).data('action');
            var resource_uri = container.data('resource_uri');

            if (action == 'delete') {
                container.remove()
                $.ajax({
                    url: resource_uri,
                    type: 'DELETE',
                    dataType: "json",
                    contentType: "application/json",
                    processData: false,
                    success: function (data) {
                        container.hide(1000)
                    },
                    async: true
                });
            }
            ;

            if (action == 'play') {

            }
            ;


        });

        // selector

        $('#playlists_inline_selector').live('change', function (e) {
            e.preventDefault();

            var resource_uri = $(this).val();

            $('.playlist_holder', self.inline_dom_element).hide();

            $.ajax({
                url: resource_uri + 'set-current/',
                type: 'GET',
                dataType: "json",
                contentType: "application/json",
                processData: false,
                success: function (data) {
                    self.load();
                },
                async: true
            });

        });


    };

    // interval
    this.set_interval = function (method, duration) {
        self.interval = setInterval(method, duration);
    };
    this.clear_interval = function (method) {
        self.interval = clearInterval(method);
    };

    this.run_interval = function () {
        self.interval_loops += 1;

        // Put functions needed in interval here
        self.update_playlists();

    };


    this.create_playlist = function (name) {

        var data = {
            'name': name,
            'type': 'basket'
        };

        // alert('create: ' + name);

        $.ajax({
            url: self.api_url,
            type: 'POST',
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            processData: false,
            success: function (data) {
                $('> div', self.inline_dom_element).remove();
                // self.run_interval();
                self.load();
            },
            async: true
        });

        // console.log('data:', data);

        // self.run_interval();
    };


    this.delete_playlist = function (id) {

        $.ajax({
            url: self.api_url + id + '/',
            type: 'DELETE',
            dataType: "json",
            contentType: "application/json",
            processData: false,
            success: function (data) {
                //$('#playlist_holder_' + id).hide(500);

                $('#playlist_holder_' + id).fadeOut(160, function () {
                    $(this).remove();
                })


                // self.update_playlists();
                self.load();
            },
            async: true
        });
    };

    this.update_playlists = function () {

    };

    /* refactored */
    this.update_playlists_callback = function (data) {
        self.update_playlist_display(data);
        self.update_playlist_selector(data);
        this.current_data = data;
    };


    this.load = function () {

        debug.debug('PlaylistUi: load');


        // get & display data
        $.getJSON(self.api_url + '?is_current=1', function (data) {

            console.log(self.api_url + '?is_current=1')

            self.update_playlist_display(data);
            this.current_data = data;

            pushy.subscribe(self.api_url + data.objects[0].id + '/', function () {
                debug.debug('pushy callback');
                self.load();
            });


            // maybe not the best way. think about alternatives...
            try {
                alibrary.playlist_editor.rebind();
            } catch (e) {
                console.log('error', e);
            }

        });


        setTimeout(function () {
            $.getJSON(self.api_url_simple + '?type__in=playlist,basket', function (data) {
                self.update_playlist_selector(data);
            });
        }, 100)


    };

    this.update_playlist_display = function (data) {


        for (var i in data.objects) {

            var item = data.objects[i];
            var target_element = $('#playlist_holder_' + item.id);


            // filter out current playlist
            if (item.is_current) {



                // var html = ich.tpl_playlists_inline({object: item});
                var html = nj.render('alibrary/nj/playlist/listing_inline.html', {
                    object: item
                });
                // console.log('item:', item)

                self.inline_dom_element.html(html);

                self.current_items[item.id] = item;

                try {
                    //console.log('trying to subscribe to pusher with: ' + item.resource_uri);
                    //pusher.subscribe(item.resource_uri, self.update_playlists);
                    pushy.subscribe(item.resource_uri, self.update_playlists);


                } catch (e) {
                    //console.log('error subscribe to pushy:', e);
                }


            } else {
                // remove item if not the current one
                target_element.remove();
            }
        }
    };

    this.update_playlist_selector = function (data) {

        // console.log(this.current_data, data)

        if (data.objects.length > 1) {

            if (!Object.equals(this.current_data, data)) {
                console.log('data changed');

                var html = ich.tpl_playlists_inline_selector(data);
                $('.playlist-selector', self.inline_dom_element.parent()).html(html);

            } else {
                console.log('data unchanged');
            }

        } else {
            $('.playlist-selector', self.inline_dom_element.parent()).html('');
        }
    };


};


CollectorApp = (function () {

    var self = this;
    this.api_url;
    this.playlist_app;

    this.active_playlist = false;

    this.use_effects = true;
    this.animation_target = ".playlist.basket";

    this.playlists_local = false;
    this.media_to_collect = false;

    this.popup_api = false;
    this.popup_container = false;

    this.init = function () {
        debug.debug('CollectorApp: init');
        this.bindings();
    };


    this.bindings = function () {


        $('body').on('click', 'a[data-action=collect]', function (e) {
            e.preventDefault();
            e.stopPropagation();

            if (self.popup_api) {
                self.popup_api.destroy();
            }

            var container = $(this).parents('.item');
            var resource_uri = container.data('resource_uri');
            var media = [];

            self.media_to_collect = false;

            // type switch
            if (container.hasClass('media')) {

                var item_id = container.data('id');
                var item_uuid = container.data('uuid');
                media.push({id: item_id, uuid: item_uuid});

                self.media_to_collect = media;

            }

            // release -> we need to get it's media first
            if (container.hasClass('release')) {

                $.ajax({
                    url: resource_uri,
                    success: function (data) {
                        for (i in data.media) {
                            var item = data.media[i];
                            media.push({id: item.id, uuid: item.uuid});
                        }
                        self.media_to_collect = media;
                    },
                    // callbacks etc
                    async: false
                });
            }

            // playlist -> we need to get it's media first
            if (container.hasClass('playlist')) {

                $.ajax({
                    url: resource_uri + '?all=1',
                    success: function (data) {

                        for (i in data.items) {
                            var item = data.items[i].item;
                            if(item.content_type == 'media') {
                                media.push({id: item.content_object.id, uuid: item.content_object.uuid});
                            }
                        }

                        self.media_to_collect = media;
                    },
                    // callbacks etc
                    async: false
                });
            }

            // special situation - action invoked from sidebar
            if($(this).hasClass('selection-required')){
                // alert('sidebar')
                _media = [];
                $('.list_body .item.selection').each(function(i, el){
                    el = $(el);
                    var item_id = el.data('id');
                    var item_uuid = el.data('uuid');
                    _media.push({id: item_id, uuid: item_uuid});

                });

                self.media_to_collect = _media;

            }

            console.log(self.media_to_collect);


            if(self.media_to_collect && self.media_to_collect.length){
                self.dialogue(e);
            }


        });


        $('__legacy__ .collectable').live('click', function (e) {


            e.preventDefault();


            // get container item
            var container = $(this).parents('.item');
            var resource_uri = container.data('resource_uri');


            items = new Array;

            // type switch
            if (container.hasClass('release')) {
                $.log('type: release')
                $.log(resource_uri);

                $.ajax({
                    url: resource_uri,
                    success: function (data) {

                        for (i in data.media) {
                            var item = data.media[i];
                            items.push(item.id);
                        }

                        self.collect(items, false);

                    },
                    async: true
                });

            }

            // type switch
            if (container.hasClass('media')) {
                var item_id = container.data('item_id');
                $.log('type: media', 'id:' + item_id);
                items.push(item_id);
                self.collect(items, false);
            }


            if (self.use_effects) {
                $('#' + container.attr('id')).effect("transfer", { to: self.animation_target }, 300);
            }

            return false;

        });

    };

    this.dialog_bindings = function (api) {

        var el = api.elements.tooltip;

        self.popup_api = api;
        self.popup_container = el;

        // remove handlers first
        el.off('click');

        // nano scroll
        $('.listing.nano', el).nanoScroller({ flash: false, preventPageScrolling: true });

        // form actions
        el.on('click', 'a[data-action]', function (e) {
            var action = $(this).data('action');
            if (action == 'cancel') {
                api.hide();
            }
            if (action == 'save') {

                var input = $('input.name', $(this).parents('.form'));
                if (input.val().length < 1) {
                    return false;
                } else {
                    self.create_playlist(input.val());
                    input.val('');
                }
            }
        });

        // item actions
        el.on('click', '.item.playlist', function (e) {

            // don't do if link clicked
            if(!$(e.target).is("a")) {

                var item = {
                    el: $(this),
                    uuid: $(this).data('uuid'),
                    id: $(this).data('id'),
                    resource_uri: $(this).data('resource_uri')
                }
                var media = self.media_to_collect;
                self.collect(item, media);
            }



        });

        // search / filter
        el.on('keyup', 'input.search', function (e) {

            var q = $(this).val();

            if(q.length < 2){
                $('.item', el).removeClass('hidden');
            } else {
                $('.item', el).addClass('hidden');
                $('.item', el).each(function(i, item){
                    var name = $(this).data('name').toLowerCase();
                    if (name.indexOf(q) != -1) {
                        $(this).removeClass('hidden');
                    }
                });
            }


        });

        $('input.search', el).focus();


        self.update_dialog_markers();

    };


    this.update_dialog_markers = function () {

        // debug.debug('update_dialog_markers');
        // debug.debug('local playlist:', self.playlists_local)
        // debug.debug('media_to_collect:', self.media_to_collect)

        var el = self.popup_container;
        var local_uuids = [];
        $.each(self.media_to_collect, function (i, media) {
            console.log(media)
            local_uuids.push(media.uuid);
        })

        console.log('media to collect, uuids:', local_uuids);

        $('.collected', el).html('');

        $.each(self.playlists_local.objects, function (i, item) {

            var container = $('.' + item.uuid, el);
            var matches = 0;

            // loop items and compare
            $.each(item.item_uuids, function (j, uuid) {

                if ($.inArray(uuid, local_uuids) > -1) {
                    matches++
                }

            })
            if (matches > 0) {
                var html = '<i class="icon icon-star"></i>';
                $('.collected', container).html(html);
                container.addClass('match');
            } else {
                container.removeClass('match');
            }


        });


    };

    this.create_playlist = function (name, type) {

        var data = {
            'name': name,
            'type': (type != undefined) ? type : 'basket'
        };

        // alert('create: ' + name);

        $.ajax({
            url: self.api_url,
            type: 'POST',
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            processData: false,
            success: function (data) {
                // self.load(true);
                debug.debug('the data:', data)
                var el = self.popup_container;
                var html = nj.render('alibrary/nj/playlist/select_popup_item.html', { item: data });

                $('.listing .content p.notice', el).fadeOut(500);

                $('.listing .content', el).append(html);
                $('.listing.nano', el).nanoScroller({ scroll: 'bottom' });

                // reset the playlist cache
                // self.playlists_local = false;

                // append to cache
                self.playlists_local.objects.push(data)

            },
            async: true
        });

        // console.log('data:', data);

        // self.run_interval();
    };

    this.get_dialog_content = function (api) {

        if (self.playlists_local) {
            setTimeout(function () {
                self.dialog_bindings(api);
            }, 10);
            return self.render_dialog_content(self.playlists_local)
        } else {
            var uri = '/api/v1/library/simpleplaylist/'
            $.ajax({
                url: uri + '?limit=500&type__in=playlist,basket',
                success: function (data) {
                    self.playlists_local = data;
                    api.set({
                        'content.text': self.render_dialog_content(self.playlists_local)
                    });
                    self.dialog_bindings(api);
                },
                async: true
            });
        }
        return '<p>loading</p>';
    };

    this.render_dialog_content = function (data) {
        var html = nj.render('alibrary/nj/playlist/select_popup.html', { data: data });
        return html;
    };


    this.dialogue = function (e) {


        $('<div />').qtip({
            content: {
                // text: nj.render('alibrary/nj/playlist/select_popup.html', { data: data }),
                text: function (e, api) {
                    return self.get_dialog_content(api);
                },
                title: false
            },
            position: {
                my: 'top right',
                at: 'bottom left',
                target: $(e.currentTarget),
                viewport: $(window),
                adjust: {
                    x: -2,
                    scroll: true,
                    resize: true,
                    method: 'flipinvert'
                }

            },
            show: {
                ready: true,
                modal: {
                    on: false,
                    blur: true
                }
            },
            hide: false,
            style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded popup-select-playlist',
            events: {
                render: function (e, api) {
                    // $('body *').click(api.hide);
                    // var tooltip = api.elements.tooltip;
                    var timeout = false;
                    $(api.elements.tooltip).on('mouseover', function () {
                        clearTimeout(timeout);
                    });
                    $(api.elements.tooltip).on('mouseleave', function () {
                        timeout = setTimeout(function () {
                            api.destroy();
                        }, 500);
                    });

                }
            }
        });
    }


    this.collect = function (item, media) {


        item.el.addClass('loading');

        var ids = [];
        $.each(media, function (i, x) {
            ids.push(x.id);
        })

        var data = {
            ids: ids.join(','),
            ct: 'media'
        }

        jQuery.ajax({
            url: item.resource_uri.replace('simple', '') + 'collect/',
            type: 'POST',
            data: data,
            dataType: "json",
            contentType: "application/json",
            //processData:  false,
            success: function (data) {
                var html = nj.render('alibrary/nj/playlist/select_popup_item.html', { item: data });
                item.el.replaceWith(html);

                var el = $('.' + data.uuid);
                el.removeClass('loading');


                // kind of hackish... loop lists, compare uuids and ev replace item
                var exists = false;
                $.each(self.playlists_local.objects, function (i, playlist) {
                    if(playlist.uuid == data.uuid) {

                        self.playlists_local.objects[i] = data;
                        exists = true;
                    }

                });

                // not found -> push to list
                if (! exists) {
                    self.playlists_local.objects.push(data)
                }

                self.dialog_bindings(self.popup_api);
            },
            async: true
        });

    };


    this.__collect = function (items) {

        var data = {
            ids: items.join(','),
            ct: 'media'
        }

        url = this.api_url + 'collect/';

        /**/
        jQuery.ajax({
            url: url,
            type: 'POST',
            data: data,
            dataType: "json",
            contentType: "application/json",
            //processData:  false,
            success: function (data) {
                if (self.playlist_app) {
                    //self.playlist_app.update_playlists();
                    self.playlist_app.load();
                }
            },
            async: true
        });

    };

});


// selector to set active playlist
// currently osed in popup-player
PlaylistSelector = function () {

    var self = this;

    this.interval = false;
    this.interval_loops = 0;
    this.interval_duration = false;
    this.api_url_simple = false; // used for listings as much faster..

    this.dom_id;
    this.dom_element;

    this.current_data;

    this.init = function () {

        $.log('PlaylistSelector: init');
        this.dom_element = $('#' + this.dom_id);

        self.iface();
        self.bindings();

        // set interval and run once
        if (self.interval_duration) {
            self.set_interval(self.run_interval, self.interval_duration);
        }
        self.run_interval();

    };

    this.iface = function () {

    };

    this.bindings = function () {
        // selector
        $('select', self.dom_element).live('change', function (e) {
            e.preventDefault();
            var resource_uri = $(this).val();

            $.ajax({
                url: resource_uri + 'set-current/',
                type: 'GET',
                dataType: "json",
                contentType: "application/json",
                processData: false,
                success: function (data) {
                    self.run_interval();
                },
                async: true
            });


        });
    };

    // interval
    this.set_interval = function (method, duration) {
        self.interval = setInterval(method, duration);
    };
    this.clear_interval = function (method) {
        self.interval = clearInterval(method);
    };

    this.run_interval = function () {
        self.interval_loops += 1;
        self.update();

    };


    this.update = function () {

        var selector = $('select', self.dom_element);

        $.getJSON(self.api_url_simple + '?type__in=playlist,basket', function (data) {

            var html = '';
            for (i in data.objects) {
                var item = data.objects[i];
                //console.log('item:', item);

                html += '<option';
                if (item.is_current) {
                    html += ' selected="selected" ';
                }
                html += ' value="' + item.resource_uri + '" ';
                html += ' >'
                html += item.name;
                html += ' [' + item.item_count + ']';
                html += '</option>';
            }
            ;
            selector.html(html);

        });
    };

};


Object.equals = function (x, y) {
    if (x === y) return true;
    // if both x and y are null or undefined and exactly the same

    if (!( x instanceof Object ) || !( y instanceof Object )) return false;
    // if they are not strictly equal, they both need to be Objects

    if (x.constructor !== y.constructor) return false;
    // they must have the exact same prototype chain, the closest we can do is
    // test there constructor.

    for (var p in x) {
        if (!x.hasOwnProperty(p)) continue;
        // other properties were tested using x.constructor === y.constructor

        if (!y.hasOwnProperty(p)) return false;
        // allows to compare x[ p ] and y[ p ] when set to undefined

        if (x[ p ] === y[ p ]) continue;
        // if they have the same strict value or identity then they are equal

        if (typeof( x[ p ] ) !== "object") return false;
        // Numbers, Strings, Functions, Booleans must be strictly equal

        if (!Object.equals(x[ p ], y[ p ])) return false;
        // Objects and Arrays must be tested recursively
    }

    for (p in y) {
        if (y.hasOwnProperty(p) && !x.hasOwnProperty(p)) return false;
        // allows x[ p ] to be set to undefined
    }
    return true;
}