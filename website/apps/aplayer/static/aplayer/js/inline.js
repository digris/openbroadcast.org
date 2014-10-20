InlinePlayer = function () {

    var self = this;
    this.item;
    this.dom_id = 'aplayer_inline';
    this.dom_element;
    this.player;

    this.state = false;
    this.source = false;
    this.current_uuid = false;
    this.current_media = false;

    this.init = function () {

        self.dom_element = $('#' + self.dom_id);
        debug.debug('InlinePlayer: init');
        self.bindings();
    };

    this.bindings = function () {
        debug.debug('InlinePlayer: bindings');
        var timeout;
        // listen for hover only on display, but hout on whole element
        $(self.dom_element).on('mouseover', 'div.display', function () {
            self.dom_element.addClass('hover');
            self.display_listing();
        });
        $(self.dom_element).on('mouseover', function () {
            if (timeout) {
                window.clearTimeout(timeout);
            }
        });
        $(self.dom_element).on('mouseleave', function () {
            self.dom_element.removeClass('hover');
            timeout = window.setTimeout(function () {
                if (!$('.popup-select-playlist').length) {
                    self.hide_listing();
                }
            }, 300)
        });


        // player actions
        $(self.dom_element).on('click', 'a[data-action]', function (e) {
            e.preventDefault();

            var action = $(this).data('action');

            debug.debug('action', action);

            if (action == 'pause') {
                self.player.base.controls({action: 'pause' });
            }

            if (action == 'play' && self.player.states.state) {
                self.player.base.controls({action: 'pause' });
            }

            if (action == 'next') {
                if (self.player.states.next) {
                    self.player.base.controls({action: 'play', index: self.player.states.next });
                }
            }

            if (action == 'prev') {
                if (self.player.states.prev !== false) { // note: in js 0 == false > true
                    self.player.base.controls({action: 'play', index: self.player.states.prev });
                }
            }


        });

        // playlist items
        $(self.dom_element).on('click', '.listing .item', function (e) {

            if ($(e.target).is("a") || $(e.target).is("i")) {

            } else {

                var uuid = $(this).attr('id');
                var index = self.player.vars.uuid_map[uuid]

                var args = {
                    action: 'play',
                    index: index
                }

                self.player.base.controls(args)

            }

        });

        // waveform cursor


        // moving & clicking the handler
        $(self.dom_element).on('mousemove', '.playhead .handler', function (e) {
            var pos = util.get_position(e);
            $(this).css('background-position', pos['x'] + 'px' + ' 0px');
        });
        $(self.dom_element).on('click', '.playhead .handler', function (e) {
            outer_width = $(this).css('width').slice(0, -2);
            base_width = outer_width;

            var pos = util.get_position(e);
            var x_percent = pos['x'] / (base_width) * 100;
            var uuid = $(this).parents('.item').attr('id');

            // trigger control
            var args = {
                action: 'seek',
                position: x_percent,
                uuid: uuid
            }
            self.player.base.controls(args);
        });


    };

    this.display_listing = function () {
        var container = $('.listing', self.dom_element);
        var container_listing = $('.inner', container);

        container_listing.html('');
        container.show();


        if (self.player && self.source == 'alibrary') {
            var playlist = self.player.vars.playlist;

            $.each(playlist, function (i, item) {

                var html = nj.render('aplayer/nj/inline_player_item.html', {
                    object: item
                });

                container_listing.append(html);

            });
        }


        if (self.player && self.source == 'abcast') {

            var html = nj.render('aplayer/nj/inline_player_item.html', {
                object: self.current_media
            });

            container_listing.append(html);


        }

    };

    this.hide_listing = function () {
        var container = $('.listing', self.dom_element);
        container.fadeOut(100);
    };


    this.update = function (aplayer, media) {


        var container = self.dom_element;
        var states = aplayer.states;


        //debug.debug('aplayer:', aplayer)
        //debug.debug('media:', media)

        if (self.state !== states.state) {
            debug.debug('state changed');
            self.state = states.state;
            self.current_media = media;
            self.update_state();
            //self.display_listing();
        }

        if (self.current_uuid !== media.uuid) {
            debug.debug('media changed');
            self.current_uuid = media.uuid;
            self.update_media();
            //self.display_listing();
        }

        // update source
        if (aplayer.vars.source) {
            // alibrary or abcast
            self.source = aplayer.vars.source
        }


        // kind of hackish... switch between alibrary and abcast
        if (aplayer.vars.source && aplayer.vars.source == 'alibrary') {
            // TODO: maybe rewrite the display section to nj templates

            container.addClass('alibrary');
            container.removeClass('abcast');

            $('li.current', container).html(util.format_time(states.position));
            $('li.total', container).html(util.format_time(states.duration));

            $('ul.timing', container).fadeIn(500);
            $('.media_name a', container).html(media.name);
            $('.media_name a', container).attr('href', media.absolute_url);

            /*
             $('.artist_name a', container).html(media.artist.name);
             $('.artist_name a', container).attr('href', media.artist.absolute_url);
             $('.release_name a', container).html(media.release.name);
             $('.release_name a', container).attr('href', media.release.absolute_url);
             */
            $('.listing .inner .indicator', container).css('width', states.position_rel + '%');


        }

        if (aplayer.vars.source && aplayer.vars.source == 'abcast') {
            // TODO: maybe rewrite the display section to nj templates

            container.addClass('abcast');
            container.removeClass('alibrary');

            $('li.current', container).html('');
            $('li.total', container).html('');
            $('ul.timing', container).hide();
            $('.media_name a', container).html(media.name);
            $('.media_name a', container).attr('href', media.absolute_url);
            $('.listing .inner .indicator', container).css('width', '0%');

        }


    };

    this.update_state = function () {
        self.dom_element.removeClass();
        self.dom_element.addClass(self.state);
    }

    this.update_media = function () {
        debug.debug('self.current_media', self.current_media)

        $('.playhead .waveform img').attr('src', self.current_media.waveform_image);
    }

    this.reset = function () {
        debug.debug('InlinePlayer: reset');
        var container = self.dom_element;

        // TODO: maybe rewrite the display section to nj templates
        $('.media_name a').html('&nbsp;');
        $('.artist_name a').html('&nbsp;');
        $('.release_name a').html('&nbsp;');
        $('ul.timing', container).fadeOut(500);

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


}




