/*
inline version - used in sidebar at some places
 */

AplayerApp = function (context) {

    var self = this;
    this.version = '0.2.17b';
    this.stream_mode = 'html5';
    this.loaded = true;
    this.states = { current: 0, next: false, prev: false};
    this.interval_duration = 500;
    this.container_id = 'aplayer_container';
    this.player;
    this.context = context;  // "main" or "popup"

    var vars = {
        swf_url: ''
    };

    this.init = function () {
        debug.debug('AplayerApp: init');

        if (self.context == 'main') {
            self.init_main();
            self.bindings_main();
        }
        if (self.context == 'popup') {
            self.init_popup();
            self.bindings_popup();
        }

    };


    /*********************************************************
     Initialisation
     *********************************************************/
    this.init_main = function () {
        debug.debug('AplayerApp: init_main');
    };

    this.init_popup = function () {
        debug.debug('AplayerApp: init_popup');
        self.player = JWP(self);
    };


    /*********************************************************
     Bindings
     *********************************************************/
    this.bindings_main = function () {
        $('body').on('click', '.playable.popup:not(".disabled")', function (e) {

            e.preventDefault();

            var ct = $(this).data('ct');
            var uri = $(this).data('resource_uri');
            var offset = $(this).data('offset');
            var mode = $(this).data('mode');
            var token = 'xx-yy-zz';
            var source = 'alibrary';

            // ct based switches
            // media set -> ignore uri and build one by ourselves
            if (ct == 'media_set') {

                // get all items currently shown
                var item_ids = [];
                var item_id = $(this).parents('.item').data('item_id');
                var container = $(this).parents('.container');

                $('.item.media', container).each(function (i, el) {
                    var current_id = $(el).data('item_id');
                    if (current_id == item_id) {
                        offset = i;
                    }
                    item_ids.push(current_id)
                })

                uri = '/api/v1/library/track/?id__in=' + item_ids.join(','); // sorry, kind of ugly..

            }

            aplayer.base.play_in_popup(uri, token, offset, mode, false, source);

            /* TESTING:
             aplayer.base.play_in_popup('/api/v1/library/track/?id__in=11,12', 'xyz', 0, 'replace', false, 'alibrary')
             http://local.openbroadcast.org:8080/api/v1/library/track/?format=json&id__in=11,12
             */

            // return false;

        });


        $('body').on('click', '.streamable.popup:not(".disabled")', function (e) {

            e.preventDefault();

            var uri = $(this).data('resource_uri');
            var offset = 0;
            var mode = 'replace';
            var token = 'xx-yy-zz';
            var source = 'abcast';

            aplayer.base.play_in_popup(uri, token, offset, mode, false, source);

        });
    };

    this.bindings_popup = function () {

    };


    this.update = function (aplayer, media) {

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


JWP = function (aplayer) {

    // kill instance
    try {
        jwplayer(aplayer.container_id).remove();
    } catch (e) {
        debug.debug(e)
    }

    // player setup
    return jwplayer(container).setup({
        id: container,
        flashplayer: aplayer.vars.swf_url,
        height: 10,
        width: 610,
        repeat: false,
        rtmp: {
            bufferlength: 1.0,
            securetoken: "Kosif093n203a"
        },
        events: {
            onReady: function () {
                //aplayer.jwp.on_ready();
            },
            onPlaylist: function (event) {
                //aplayer.jwp.on_playlist(event);
            },
            onComplete: function (event) {
                //aplayer.jwp.on_complete(event);
            }
        },
        modes: [
            {type: 'flash', src: aplayer.vars.swf_url},
            {type: 'html5'}
        ],
    });
}



