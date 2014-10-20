/*
 * PLAYLIST EDITOR
 */


PlaylistEditor = function () {

    var self = this;

    this.interval = false;
    this.interval_loops = 0;
    this.interval_duration = 30000;
    //this.interval_duration = false;
    this.api_url = false;
    this.uuid = 'sdkhj';
    this.dom_id = 'playlist_editor_list';
    this.dom_element;

    this.mode;

    // readonly mode for locked playlists
    this.readonly = false;
    this.enable_crossfades = false;

    // holding the playlist
    this.current_playlist;
    // local cache of items
    this.current_items = new Array;
    // holding the objects
    this.editor_items = new Array;

    this.current_waveforms = new Array;
    this.uuid_map = new Array();
    this.position_map = new Array();

    this.input_blur = new Array;

    this.init = function () {

        debug.debug('PlaylistEditor: init');
        debug.debug(self.api_url);

        self.dom_element = $('#' + this.dom_id);

        self.iface();
        self.bindings();

        // set subscription, if failed an interval and run once
        try {
            pushy.subscribe(self.api_url, self.update);
        } catch (e) {

            debug.debug('error', e);

            if (self.interval_duration) {
                self.set_interval(self.run_interval, self.interval_duration);
            }
        }
        self.run_interval();

    };

    // just testing
    this.update = function () {
        self.run_interval();
    }

    this.iface = function () {
        // this.floating_inline('lookup_providers', 120)
    };

    this.bindings = function () {


        /*
         * Playlist main-editor
         */

        if (!self.readonly) {
            self.dom_element.sortable(
                {
                    placeholder: "item drop-placeholder",
                    axis: "y",
                    cursor: "move",
                    //cursorAt: { left: 5 },
                    delay: 150,
                    handle: '.base',
                    scroll: true,
                    scrollSensitivity: 10
                }
            );

            self.dom_element.disableSelection();
        }
        ;


        self.dom_element.on("sortupdate", function (e, ui) {

            var dom_item = $(ui.item[0]);

            // check if dropped from outside
            if (dom_item.hasClass('sidebar list item source')) {

                debug.debug('dropped from outside');

                var post_data = {};

                // get item details
                jQuery.ajax({
                    url: dom_item.data('resource_uri'),
                    type: 'GET',
                    dataType: "json",
                    contentType: "application/json",
                    //processData:  false,
                    success: function (data) {
                        debug.debug(data);
                        try {
                            post_data = {
                                ids: [data.item.object_id].join(','),
                                ct: data.item.content_type
                            }
                        } catch (e) {
                            post_data = {
                                ids: [data.id].join(','),
                                // TODO: modularize: expose type in api
                                ct: 'jingle'
                            }
                        }
                        ;
                    },
                    async: false
                });

                // add item to current playlist (the one in the main editor)
                url = self.api_url + 'collect/';
                var data;
                jQuery.ajax({
                    url: url,
                    type: 'POST',
                    data: post_data,
                    dataType: "json",
                    contentType: "application/json",
                    //processData:  false,
                    success: function (data) {


                        var item = data.items.pop();

                        debug.debug('created item:', item);

                        //data = data;
                        var temp_html = '<div class="temporary item editable" id="playlist_item_' + item.id + '" data-uuid="' + item.uuid + '"><i class="icon-spinner icon-spin icon-2x"></i></div>'
                        dom_item.replaceWith(temp_html);

                    },
                    async: false
                });


                // create an entry in the editor list (uuid used for reordering)


            }
            ;


            if (ui.sender && ui.sender[0].id == 'jingle_list') {
                debug.debug('jingle dropped!!');
            }

            if (ui.sender && ui.sender[0].id == 'inline_playlist_holder') {
                debug.debug('jingle dropped!!');
            }

            self.reorder();

        });


        $('.item.editable input', self.dom_element)
            .live('blur', function (e) {

                var container = $(this).parents('.item');
                var uuid = container.data('uuid');
                debug.debug(uuid + ' - blur');
                self.input_blur[uuid] = setTimeout(function () {
                    debug.debug('blur - timeout -> post')
                    container.trigger('blur_batch')
                }, 100)

            })
            .live('focus', function (e) {

                var container = $(this).parents('.item');
                var uuid = container.data('uuid');
                debug.debug(uuid + ' - focus');

                // clearTimeout(self.input_blur[uuid]);

            })
        $('.item.editable', self.dom_element).live('blur_batch', function (e) {
            debug.debug('blur_batch triggered!');

            self.update_by_uuid($(this).data('uuid'));
        });


        // mode switch TODO: improve
        $('#editor_mode_switch a', $('#playlist_editor')).live('click', function (e) {
            e.preventDefault();

            var mode = $(this).data('mode');
            $('#playlist_editor').removeClass('condensed extended');
            $('#playlist_editor').addClass(mode);


        });


        /*
         * playlist autocompletion
         * to search libraery for more tracks & adding them to the current playlist
         */

        // autocomplete search box TODO: maybe move
        self.ac = new AutocompleteApp();
        self.ac.api_url = '/api/v1/library/track/autocomplete/';
        self.ac.container = $("#playlist_editor_search .result");
        this.ac.template = 'alibrary/nj/playlist/editor_search.html';

        // state toggler
        $("#playlist_editor_search")
            .on('focus', 'input',function (e) {
                $(this).parents('#playlist_editor_search').addClass('focus');
            }).on('blur', 'input', function (e) {
                $(this).parents('#playlist_editor_search').removeClass('focus');
            });


        // Select on 'ENTER' >TODO: implement
        $("#playlist_editor_search").on('keyup', 'input', function (e) {

            var q = $(this).val();


            if (e.keyCode == 13 || e.keyCode == 9) {
                // e.preventDefault();
                var uri = util.uri_param_insert(window.location.href, 'q', q, true);
                uri = util.uri_param_insert(uri, 'page', 1, true);
                window.location = uri;
                return false;
            } else {

                debug.debug(q);
                self.ac.search(q);

            }

        });

        // add selected item
        $("#playlist_editor_search").on('click', '.result .item', function (e) {

            // get item details
            $.ajax({
                url: $(this).data('resource_uri'),
                type: 'GET',
                dataType: "json",
                contentType: "application/json",
                success: function (data) {
                    $.ajax({
                        url: self.api_url + 'collect/',
                        type: 'POST',
                        data: {
                            ids: [data.id].join(','),
                            ct: 'media'
                        },
                        dataType: "json",
                        contentType: "application/json",
                        success: function (data) {
                            var item = data.items.pop();
                            debug.debug('created item:', item);
                            //data = data;
                            var html = '<div class="temporary item editable" id="playlist_item_' + item.id + '" data-uuid="' + item.uuid + '"><i class="icon-spinner icon-spin icon-2x"></i></div>'
                            $('#playlist_editor_list').append(html);

                            // reset
                            $('input', $('#playlist_editor_search')).val('');
                            $('.result', $('#playlist_editor_search')).html('');

                            self.reorder();
                        }
                    });

                }
            });

        });


        this.rebind();

    };

    this.rebind = function () {

        /*
         * Sidebar, dragable playlists (a.k.a. baskets)
         */
        $('#inline_playlist_holder .list').sortable({
            placeholder: "item drop-placeholder",
            connectWith: self.dom_element,
            helper: "clone"
        });

        $('#inline_jingle_holder .list').sortable({
            placeholder: "item drop-placeholder",
            connectWith: self.dom_element,
            helper: "clone"
        });

    };

    this.reorder = function () {

        // numbering
        var reorder_url = self.current_playlist.resource_uri + 'reorder/';

        var order = new Array;

        $('.item.editable').each(function (i, e) {

            order.push($(e).data('uuid'));
            $('span.pos_new', $(this)).html(i);

        });

        debug.debug('order:', order);

        $.ajax({
            url: reorder_url,
            type: 'POST',
            data: { order: order.join(',') },
            success: function (data) {
                self.run_interval();
            },
            async: false
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
        self.update_editor();
    };


    // update data by uuid (using uuid mapping)
    this.update_by_uuid = function (uuid, refresh_item) {

        var item = self.current_playlist.items[self.uuid_map[uuid]];
        var container = $('.' + uuid, this.dom_element);

        debug.debug('container', container);

        // aquire data
        var fade_in = $('input.fade_in', container).val();
        var fade_out = $('input.fade_out', container).val();
        var fade_cross = $('input.fade_cross', container).val();
        var cue_in = $('input.cue_in', container).val();
        var cue_out = $('input.cue_out', container).val();

        delete item.item.content_object;
        delete item.item.content_type;

        debug.debug('fade_in:', fade_in)
        debug.debug('fade_out:', fade_out)

        item.fade_in = fade_in;
        item.fade_out = fade_out;
        item.fade_cross = fade_cross;
        item.cue_in = cue_in;
        item.cue_out = cue_out;

        debug.debug('pre-post');
        $.ajax({
            url: item.resource_uri,
            type: 'PUT',
            data: JSON.stringify(item),
            dataType: "json",
            contentType: "application/json",
            processData: false,
            success: function (data) {
                // debug.debug('data:', data);
                if (refresh_item == true) {
                    debug.debug(self.editor_items);
                    // TODO: not working
                    self.editor_items[item.id].update(item, self);
                }

            },
            async: false
        });
        debug.debug('post-post');

        self.run_interval();

    };

    this.update_editor = function () {
        $.getJSON(self.api_url, function (data) {
            self.current_playlist = data;

            for (i in data.items) {
                item = data.items[i];
                self.uuid_map[item.uuid] = i;
                self.position_map[item.position] = item.id;
            }

            // main editor
            self.update_editor_playlist(data);

            // self.update_editor_summary(data);
            self.update_editor_transform(data);
            self.rebind();
        });
    };


    this.update_editor_transform = function (data) {
        /*
        most information is displayed while page rendering. just override some states for duration
         */
        debug.debug('update_editor_summary')
        debug.debug(data)

        var container = $('.criterias-broadcast');

        var total_duration = 0;
        for (i in self.current_items) {
            if (isInt(i)) {
                var item = self.current_items[i];
                total_duration += item.item.content_object.duration;
                total_duration -= (item.cue_in + item.cue_out + item.fade_cross);
            }
        }

        var error = true;
        if (Math.abs(self.current_playlist.target_duration * 1000 - total_duration) < 2000) {
            error = false;
        } else {
            error = 'Durations do not match.'
        }

        var durations = {
            total: total_duration,
            target: self.current_playlist.target_duration * 1000,
            difference: self.current_playlist.target_duration * 1000 - total_duration,
            error: error
        }


        debug.debug('durations', durations)


        html = nj.render('alibrary/nj/playlist/_transform_duration.html', {
            durations: durations
        });

        $('.criteria.duration', container).replaceWith(html);

        /**/
        if (error) {
            $('.link a', container).addClass('disabled');
        } else {
            $('.link a', container).removeClass('disabled');
        }



    };

    this.update_editor_playlist = function (data) {

        // debug.debug(data)

        var status_map = new Array;
        status_map[0] = 'init';
        status_map[1] = 'done';
        status_map[2] = 'ready';
        status_map[3] = 'progress';
        status_map[4] = 'downloaded';
        status_map[99] = 'error';


        for (var i in data.items) {

            var item = data.items[i];


            if (isInt(i)) {

                var content_type = item.item.content_type;
                var target_element = $('#playlist_item_' + item.id);

                item.status_key = status_map[item.status];

                if (item.id in self.current_items) {
                    // already here
                    if (item.updated != self.current_items[item.id].updated) {
                        this.editor_items[item.id].update(item, self);
                    }

                } else {

                    if (content_type == 'media') {
                        this.editor_items[item.id] = new PlaylistEditorItem();
                        this.editor_items[item.id].init(item, self);
                    }

                    if (content_type == 'jingle') {
                        this.editor_items[item.id] = new PlaylistEditorItem();
                        this.editor_items[item.id].init(item, self);
                    }

                }

                self.current_items[item.id] = item;
            }


        }

    };


    // play-flow functions
    this.play_next = function (current_id) {

        //debug.debug('play next');

        // get ordered list

        var order = new Array;

        $('.item.editable').each(function (i, e) {
            order.push($(e).data('id'));
        });

        //debug.debug(self.position_map);
        //debug.debug(self.editor_items);

        var current_item_id = self.position_map.indexOf(current_id);
        var next_item_id = self.position_map[current_item_id + 1];
        var next_item = this.editor_items[next_item_id];

        next_item.player.play();

    };
    // play-flow functions
    this.load_next = function (current_id) {

        // debug.debug('load next');

        // get ordered list

        var order = new Array;

        $('.item.editable').each(function (i, e) {
            order.push($(e).data('id'));
        });

        //debug.debug(self.position_map);
        //debug.debug(self.editor_items);

        var current_item_id = self.position_map.indexOf(current_id);
        var next_item_id = self.position_map[current_item_id + 1];
        var next_item = this.editor_items[next_item_id];

        next_item.player.load();

    };

    // play-flow functions
    this.stop_all = function () {

        for (var i in this.editor_items) {
            if (isInt(i)) {
                this.editor_items[i].player.stop();
            }
        }

    };


};


PlaylistEditorItem = function () {

    var self = this;
    this.api_url = false;

    this.item;
    this.playlist_editor;
    this.dom_id;
    this.waveform_dom_id;
    this.dom_element;
    this.ct;
    this.co;

    // readonly mode for locked playlists
    this.readonly = false;
    this.enable_crossfades = false;
    this.enable_drag_n_drop = false;

    this.el_background;
    this.el_buffer;
    this.el_indicator;
    this.el_controls_cross;
    this.el_waveform;
    this.el_envelope;
    this.el_controls_fade;
    this.el_controls_cue;
    this.el_controls_fade_cross;

    this.player;

    this.envelope_color = '#00bb00';
    this.waveform_fill = '90-#aaa-#444:50-#aaa';


    this.interval_duration = false;
    self.interval_loops;

    this.duration = 0;

    this.state;

    this.size_x = 830;
    this.size_y = 30;
    this.envelope_top = 8;
    this.envelope_bottom = 6;

    this.r;

    self.editor_container = $('#playlist_editor_list');

    this.listeners;


    this.init = function (item, playlist_editor) {

        self.item = item;
        this.playlist_editor = playlist_editor;
        this.readonly = playlist_editor.readonly;
        this.enable_crossfades = playlist_editor.enable_crossfades;

        //debug.debug('PlaylistEditorItem - init');
        self.api_url = self.item.resource_uri;
        self.ct = self.item.item.content_type;
        self.co = self.item.item.content_object;

        self.state = 'init';

        var html = '';
        if (self.ct == 'media') {

            html = nj.render('alibrary/nj/playlist/editor_item.html', {
                object: self.item,
                readonly: self.readonly,
                enable_crossfades: self.enable_crossfades
            });
        }

        if (self.ct == 'jingle') {

            this.waveform_fill = '90-#aaa-#63c:50-#aaa';

            html = nj.render('alibrary/nj/playlist/editor_item.html', {
                object: self.item,
                readonly: self.readonly
            });
        }

        // check if append or replace
        if ($('#playlist_item_' + self.item.id).length) {
            debug.debug('!!! replacing item !!!')
            $('#playlist_item_' + self.item.id).replaceWith(html);
        } else {
            self.editor_container.append(html);
        }


        self.dom_id = 'playlist_item_' + self.item.id;
        self.dom_element = $('#' + self.dom_id);
        self.dom_element.css('height', self.size_y + 70);
        self.waveform_dom_id = 'playlist_item_waveform_' + self.item.id;

        self.bindings();
        self.init_waveform();
        self.init_player();

        // set interval and run once
        // TODO: do we need this?
        if (self.interval_duration) {
            self.set_interval(self.run_interval, self.interval_duration);
        }
        // self.run_interval();


    };

    this.bindings = function () {


        // hover mapping
        $(self.dom_element).live('mouseenter', function (e) {
            self.trigger_hover(e);
        });

        $(self.dom_element).live('mouseleave', function (e) {
            self.trigger_hout(e);
        });


        $('.waveform', self.dom_element).live('click', function (e) {
            debug.debug(e.offsetX);
            debug.debug(self.px_to_abs(e.offsetX));

            self.player.setPosition(self.px_to_abs(e.offsetX));

        });

        $('.actions a', self.dom_element).live('click', function (e) {
            e.preventDefault();

            var action = $(this).data('action');

            if (action == 'delete' && confirm('sure?')) {
                $.ajax({
                    url: self.item.resource_uri,
                    type: 'DELETE',
                    dataType: "json",
                    contentType: "application/json",
                    processData: false,
                    success: function (data) {
                        self.dom_element.remove();
                        delete self.playlist_editor.current_items[self.item.id]
                        delete self.playlist_editor.editor_items[self.item.id]
                        self.playlist_editor.reorder();
                    },
                    async: false
                });
            }
            ;

            if (action == 'play') {


                // try to pause aplayer - hackish..
                try {
                    if (aplayer.inline.player.states.state == 'playing') {
                        aplayer.inline.player.base.controls({action: 'pause' })
                    }
                } catch (e) {

                }
                ;

                self.playlist_editor.stop_all();
                self.player.play().setPosition(self.item.cue_in);
            }
            ;
            if (action == 'pause') {
                self.player.togglePause();
            }
            ;
            if (action == 'stop') {
                self.player.stop();
            }
            ;

        });

        $('a.editor.preview', self.dom_element).live('click', function (e) {
            e.preventDefault();

            var preview = $(this).data('preview');

            var pos = 0;

            self.playlist_editor.stop_all();


            if (preview == 'fade_cross') {
                pos = self.co.duration - self.item.cue_out - self.item.fade_cross - 2000;
            }
            ;

            if (preview == 'fade_in') {
                pos = self.item.cue_in;
            }
            ;

            if (preview == 'fade_out') {
                if (self.item.fade_cross > self.item.fade_out) {
                    pos = self.co.duration - self.item.cue_out - self.item.fade_cross - 2000;
                } else {
                    pos = self.co.duration - self.item.cue_out - self.item.fade_out - 2000;
                }
            }
            ;

            self.player.play().setPosition(pos);

        });


    }

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
        //debug.debug('run_interval');
        //debug.debug(self.player);

        var paused = self.player.paused;
        var playState = self.player.playState;
        //debug.debug('paused: ', paused);
        //debug.debug('playState: ', playState);

        if (paused) {
            self.dom_element.addClass('paused');
        } else {
            self.dom_element.removeClass('paused');
        }

    };

    this.update = function (item, playlist_editor) {
        debug.debug('PlaylistEditorItem - update');
        self.item = item;
        this.playlist_editor = playlist_editor;

        // self.el_indicator.rotate(30)
        var x = self.get_x_points();
        var path = self.get_path(x);
        this.el_envelope.animate({path: path}, 0);


        self.el_buffer.attr({x: self.abs_to_px(self.item.cue_in), width: self.size_x - self.abs_to_px(self.item.cue_in + self.item.cue_out)});

        // update fades
        if (self.item.fade_cross && self.item.fade_cross > 0) {
            this.el_controls_cross.animate({x: self.abs_to_px(self.co.duration - self.item.cue_out - self.item.fade_cross - 1)}, 100);
        }

        // update cues
        try {
            self.el_controls_cue[0].transform('T' + Math.floor(self.abs_to_px(self.item.cue_in)) + ',0');
        } catch (e) {

        }


        /*
         var temp = self.el_controls_cue[0].clone();
         temp.transform('t' + Math.floor(self.abs_to_px(self.item.cue_in)) + ',0');
         self.el_controls_cue[0].animate({path: temp.attr('path')}, 100);
         temp.remove();
         */

        // this.player.unload();

    };

    this.trigger_hover = function (e) {
        //debug.debug('el hover', e);
        if (self.el_controls_cue) {
            self.el_controls_cue.attr({stroke: self.envelope_color});
        }

    }
    this.trigger_hout = function (e) {
        //debug.debug('el hout', e);
        if (self.el_controls_cue) {
            self.el_controls_cue.attr({stroke: "none"});
        }

    }

    this.init_waveform = function () {


        var waveform_image = self.item.item.content_object.waveform_image;

        this.r = Raphael(self.waveform_dom_id, 830, self.size_y + 6);

        self.el_background = this.r.rect(0, 0, self.size_x, self.size_y).attr({ stroke: "none", fill: '90-#efefef-#bbb:50-#efefef' });
        self.el_buffer = this.r.rect(0, 0, 0, self.size_y).attr({ stroke: "none", fill: self.waveform_fill });
        if(waveform_image) {
            self.el_waveform = this.r.image(waveform_image, 0, 0, 830, self.size_y);
        }
        self.el_indicator = this.r.rect(-10, 0, 2, 40).attr({ stroke: "none", fill: '#00bb00' });

        self.set_envelope(true);

    };

    this.set_envelope = function (rw) {


        var x = self.get_x_points();
        var path = self.get_path(x);

        self.el_envelope = this.r.path(path).attr({stroke: self.envelope_color, "stroke-width": 1, 'opacity': 1, "stroke-linecap": "round"});


        if (!self.readonly === true) {

            /*
             * cue handling
             */

            if(self.enable_drag_n_drop) {
                var c_cue_size = 8;
                var c_cue_attr = { stroke: self.envelope_color, 'stroke-width': 2, 'fill-opacity': .1, r: 0, cursor: 'move'};

                var cp = [];
                cp[0] = [
                    ["M", c_cue_size, 2],
                    ["L", 0, 2],
                    ["L", 0, self.size_y],
                    ["L", c_cue_size, self.size_y]
                ];
                cp[1] = [
                    ["M", 0, 2],
                    ["L", c_cue_size, 2],
                    ["L", c_cue_size, self.size_y],
                    ["L", 0, self.size_y]
                ];

                self.el_controls_cue = this.r.set(
                        this.r.path(cp[0]).attr(c_cue_attr),
                        this.r.path(cp[1]).attr(c_cue_attr)
                    ).mouseover(function (set) {
                        debug.debug('set', set)
                        this.animate({"fill-opacity": .55, fill: self.envelope_color}, 100);
                    }).mouseout(function () {
                        this.animate(c_cue_attr, 300);
                    });

                // specific update functions
                self.el_controls_cue[0].update = function (x, y) {
                    // get X
                    var X = this.transform()[0][1] + x;

                    // set envelope
                    path[1][1] = X + self.abs_to_px(self.item.fade_in);
                    path[0][1] = X;
                    self.el_envelope.animate({path: path}, 0);

                    // set envelope controls
                    self.el_controls_fade[0].attr({x: X + self.abs_to_px(self.item.fade_in)});

                    // set self + update display
                    this.transform('T' + X + ',0')
                    $('.cue_in', self.dom_element).val(Math.floor(self.px_to_abs(X)));
                };
                self.el_controls_cue[1].update = function (x, y) {
                    // get X
                    var X = this.transform()[0][1] + x;

                    // set envelope
                    path[2][1] = X - self.abs_to_px(self.item.fade_out);
                    path[3][1] = X;
                    self.el_envelope.animate({path: path}, 0);

                    // set envelope controls
                    self.el_controls_fade[1].attr({x: X - self.abs_to_px(self.item.fade_out)});

                    // set self + update display
                    this.transform('T' + X + ',0')
                    $('.cue_out', self.dom_element).val(Math.floor(self.co.duration - self.px_to_abs(X + c_cue_size)));
                };

                // transform to current values
                self.el_controls_cue[0].transform('T' + x[0] + ',0');
                self.el_controls_cue[1].transform('T' + (x[3] - c_cue_size ) + ',0');
                self.el_controls_cue.drag(self.controls_cue_onmove, self.controls_cue_onstart, self.controls_cue_onend);
            }

            /*
             * fade handling
             */

            if(self.enable_drag_n_drop) {
                var c_fade_size = 6;
                var c_fade_attr = { fill: self.envelope_color, 'stroke-width': 10, 'stroke-opacity': .20, r: 1, cursor: 'move'};

                self.el_controls_fade = this.r.set(
                        this.r.rect(x[1] - c_fade_size / 2, this.envelope_top - c_fade_size / 2, c_fade_size, c_fade_size).attr(c_fade_attr),
                        this.r.rect(x[2] - c_fade_size / 2, this.envelope_top - c_fade_size / 2, c_fade_size, c_fade_size).attr(c_fade_attr)
                    ).mouseover(function () {
                        this.animate({"stroke-opacity": .75, stroke: self.envelope_color}, 100);
                    }).mouseout(function () {
                        this.animate(c_fade_attr, 300);
                    });

                // specific update functions
                self.el_controls_fade[0].update = function (x, y) {
                    var X = this.attr("x") + x, Y = this.attr("y") + y;
                    this.attr({x: X});
                    path[1][1] = X;
                    self.el_envelope.animate({path: path}, 0);
                    $('.fade_in', self.dom_element).val(Math.floor(self.px_to_abs(X)) - self.item.cue_in);
                };
                self.el_controls_fade[1].update = function (x, y) {
                    var X = this.attr("x") + x, Y = this.attr("y") + y;
                    this.attr({x: X});
                    path[2][1] = X;
                    self.el_envelope.animate({path: path}, 0);
                    $('.fade_out', self.dom_element).val(Math.floor(self.co.duration - self.px_to_abs(X)) - self.item.cue_out);
                };
                self.el_controls_fade.drag(self.controls_fade_onmove, self.controls_fade_onstart, self.controls_fade_onend);
                self.el_controls_fade.dblclick(self.controls_fade_dbclick);
            }


            // crossfade handler
            if(self.enable_crossfades){
                var c_cross_size = 8;
                var c_cross_attr = { y: self.size_y - 2, height: 12, stroke: "red", 'stroke-opacity': 0.1, 'stroke-width': 8, fill: '#ff0000', cursor: 'move'};


                self.el_controls_cross = this.r.rect(-10, self.size_y - 2, 2, self.size_y + 6).attr(c_cross_attr)
                    .mouseover(function (set) {
                        this.animate({"fill-opacity": .55, y: 0, height: self.size_y + 6}, 100);
                    }).mouseout(function () {
                        this.animate(c_cross_attr, 300);
                    });


                self.el_controls_cross.update = function (x, y) {
                    var X = this.attr("x") + x, Y = this.attr("y") + y;
                    this.attr({x: X});
                    $('.fade_cross', self.dom_element).val(self.co.duration - (Math.floor(self.px_to_abs(X)) + self.item.cue_out));
                };

                if (self.item.fade_cross && self.item.fade_cross > 0) {
                    this.el_controls_cross.animate({x: self.abs_to_px(self.co.duration - self.item.cue_out - self.item.fade_cross - 1)}, 100);
                } else {
                    this.el_controls_cross.animate({x: self.abs_to_px(self.co.duration) - 2}, 100);
                }

                self.el_controls_cross.drag(self.controls_cross_onmove, self.controls_cross_onstart, self.controls_cross_onend);
            }

        }


    };


    // fade handlers
    this.controls_fade_onmove = function (dx, dy) {
        this.update(dx - (this.dx || 0), dy - (this.dy || 0));
        this.dx = dx;
        this.dy = dy;
    }

    this.controls_fade_onstart = function (x, y) {
        debug.debug('controls_fade_onstart', x, y);
    }

    this.controls_fade_onend = function (e) {
        debug.debug('controls_fade_onend', e.offsetX);
        this.dx = this.dy = 0;
        var pos_new = e.offsetX;
        self.playlist_editor.update_by_uuid(self.item.uuid);
    }


    this.controls_fade_dbclick = function (e) {
        debug.debug('dbclick', this);
        self.item.fade_in = prompt('fade-in', self.item.fade_in);
        $('.fade_in', self.dom_element).val(Math.floor(self.item.fade_in));
        self.playlist_editor.update_by_uuid(self.item.uuid, true);
    }


    // cue handlers
    this.controls_cue_onmove = function (dx, dy) {
        this.update(dx - (this.dx || 0), dy - (this.dy || 0));
        this.dx = dx;
        this.dy = dy;
    }

    this.controls_cue_onstart = function (x, y) {
        debug.debug('controls_cue_onstart', x, y);
    }

    this.controls_cue_onend = function (e) {
        debug.debug('controls_cue_onend', e.offsetX);
        this.dx = this.dy = 0;
        var pos_new = e.offsetX;
        self.playlist_editor.update_by_uuid(self.item.uuid);
    }


    // cross handlers
    this.controls_cross_onmove = function (dx, dy) {
        this.update(dx - (this.dx || 0), dy - (this.dy || 0));
        this.dx = dx;
        this.dy = dy;
    }

    this.controls_cross_onstart = function (x, y) {
        debug.debug('controls_fade_onstart', x, y);
    }

    this.controls_cross_onend = function (e) {
        debug.debug('controls_fade_onend', e.offsetX);
        self.playlist_editor.update_by_uuid(self.item.uuid);
    }


    // validators
    this.validate_fade = function(pos_new) {

        debug.debug(pos_new);

        return false;
    };



    this.get_x_points = function () {

        var x0 = self.abs_to_px(self.item.cue_in);
        var x1 = self.abs_to_px(self.item.cue_in + self.item.fade_in);

        var x2 = self.abs_to_px(self.co.duration - self.item.cue_out - self.item.fade_out)
        var x3 = self.abs_to_px(self.co.duration - self.item.cue_out)

        return [x0, x1, x2, x3]

    };

    this.get_path = function (x) {


        var diff = x[1] - x[0]

        var p0 = ["M", x[0], this.size_y - 1];
        var p1 = ["T", x[1], this.envelope_top];
        // var p1 = ["C", x[1] - diff / 1.5, this.envelope_top + 4, x[1] - diff / 4, this.envelope_top + 1, x[1], this.envelope_top];
        var p2 = ["L", x[2], this.envelope_top];
        var p3 = ["T", x[3], this.size_y - 1];

        return [p0, p1, p2, p3]

    };

    this.abs_to_px = function (abs) {

        return self.size_x / self.co.duration * abs;

    };

    this.px_to_abs = function (px) {

        return Number(px / self.size_x * self.co.duration);

        // return self.size_x / self.co.duration * abs;

    };


    this.events = {

        classes: ['playing', 'paused'],

        play: function () {
            debug.debug('events: ', 'play');
            self.dom_element.removeClass('paused');
            self.dom_element.addClass('playing');
        },

        stop: function () {
            debug.debug('events: ', 'stop');
            self.dom_element.removeClass('paused');
            self.dom_element.removeClass('playing');

            self.el_indicator.attr({x: -10})
        },

        pause: function () {
            debug.debug('events: ', 'pause');
            self.dom_element.removeClass('playing');
            self.dom_element.addClass('paused');
        },

        resume: function () {
            debug.debug('events: ', 'resume');
            self.dom_element.removeClass('paused');
            self.dom_element.addClass('playing');
        },

        finish: function () {
            debug.debug('events: ', 'finish');
            self.dom_element.removeClass('paused');
            self.dom_element.removeClass('playing');
        }
    }


    this.init_player = function () {


        var options = {
            id: 'player_' + self.item.id,
            url: self.co.stream.uri,
            multiShot: false,
            // autoPlay: true,
            autoLoad: false,
            // events
            onplay: self.events.play,
            onstop: self.events.stop,
            onpause: self.events.pause,
            onresume: self.events.resume,
            onfinish: self.events.finish,

            whileloading: this.whileloading,
            whileplaying: this.whileplaying,
            onload: this.onload
        }

        /*
         # id:o.id,
         # url:decodeURI(soundURL),
         onplay:self.events.play,
         onstop:self.events.stop,
         onpause:self.events.pause,
         onresume:self.events.resume,
         onfinish:self.events.finish,
         whileloading:self.events.whileloading,
         whileplaying:self.events.whileplaying,
         onmetadata:self.events.metadata,
         onload:self.events.onload
         */

        soundManager.setup({debugMode: false})

        self.player = soundManager.createSound(options);
    };


    this.whileloading = function () {
        var p = self.player.bytesTotal / self.player.bytesLoaded
        self.el_buffer.attr({width: p * self.size_x});
    };


    this.whileplaying = function () {
        self.el_indicator.attr({ x: self.abs_to_px(self.player.position) });

        // check for neccessary fade

        // debug.debug('pos:', self.player.position, self.item.cue_in);

        var vol = 0;
        // ins
        if (self.player.position < self.item.cue_in) {
            vol = 5;
            self.player.setPosition(self.item.cue_in);
        }
        if (self.player.position > (self.item.cue_in + self.item.fade_in )) {
            vol = 100;
        }
        if (self.player.position > (self.item.cue_in) && self.player.position < (self.item.cue_in + self.item.fade_in )) {
            var diff = self.player.position - self.item.cue_in;
            var p = diff / self.item.fade_in;
            vol = 100 * p;
        }

        // outs
        // ins
        if (self.player.position >= self.co.duration - self.item.cue_out) {
            vol = 0;
            // self.player.setPosition(self.item.cue_in);

            setTimeout(function () {
                self.player.stop();
            }, 100);

        }
        if (self.player.position <= self.co.duration - self.item.cue_out && self.player.position > self.co.duration - self.item.cue_out - self.item.fade_out) {
            var diff = self.co.duration - self.item.cue_out - self.player.position;
            // debug.debug('t/diff:', diff);


            var p = diff / self.item.fade_out;
            vol = 100 * p;
        }

        // check for next
        var remaining = self.co.duration - (self.item.cue_out) - self.player.position;

        // debug.debug('remaining:', remaining);
        // preload next track
        if (remaining <= self.item.fade_cross + 10000) {
            self.playlist_editor.load_next(self.item.id);
        }

        if (remaining <= self.item.fade_cross + 100) {
            self.playlist_editor.play_next(self.item.id);
        }


        self.player.setVolume(vol);

    };


    this.onload = function () {

        // / debug.debug('sm2 onload');

        self.el_buffer.attr({x: self.abs_to_px(self.item.cue_in), width: self.size_x - self.abs_to_px(self.item.cue_in + self.item.cue_out)});


    };


}

