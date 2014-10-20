DetailPlayer = function () {

    var self = this;
    this.api_url = false;

    this.item;
    this.dom_id;
    this.dom_element;
    this.waveform_dom_id;
    this.api_url;

    this.el_background;
    this.el_buffer;
    this.el_waveform;
    this.el_indicator;
    this.player;
    this.aplayer_states;
    this.waveform_fill = '90-#999-#444:50-#999';
    this.state;

    this.perms = {};

    this.size_x = 810;
    this.size_y = 80;
    this.envelope_top = 8;
    this.envelope_bottom = 6;

    this.r;

    this.listeners;


    this.init = function () {

        self.dom_element = $('#' + self.dom_id);

        debug.debug('DetailPlayer: init')
        debug.debug(self.api_url)

        self.bindings();
        //self.init_waveform();
        //self.init_player();

        // self.load();

        $.get(self.api_url, function (data) {
            debug.debug('detail player - current item: ', data);
            self.init_player(data);
        })


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
            // debug.debug(e.offsetX);
            // debug.debug(self.px_to_abs(e.offsetX));

            var pos = Number(e.offsetX / self.size_x * self.item.duration / 1000);

            // check if media is currently playing

            // debug.debug('playing item:', self.aplayer_states.uuid);
            // debug.debug('seeking item:', self.item.uuid)

            if (self.item && self.aplayer_states && self.aplayer_states.uuid == self.item.uuid) {
                self.player.seek(pos);
            }



        });

        $('.actions a', self.dom_element).live('click', function (e) {
            e.preventDefault();

            var action = $(this).data('action');

            if (action == 'play') {
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

    };


    this.trigger_hover = function (e) {
        //self.el_controls_cue.attr({stroke: self.envelope_color});
        //$('.player_actions').fadeIn(100);
    };
    this.trigger_hout = function (e) {
        //$('.player_actions').fadeOut(100);
    };


    /*
     this.load = function() {

     $.get(self.api_url, function(data){
     debug.debug('detail player - current item: ', data);
     })

     };
     */


    this.init_player = function (data) {

        var html = nj.render('aplayer/nj/detail_player.html', {
            object: data,
            perms: self.perms
        });

        self.dom_element.html(html);
        self.waveform_dom_id = 'detail_player_waveform_' + data.id;

        self.item = data;

        self.init_waveform();

        // dummy mapping
        if (data.sections) {
            var sections = JSON.parse(data.sections);
            self.init_markers(sections);
        }
    };


    this.init_waveform = function () {

        var waveform_image = self.item.waveform_image;

        this.r = Raphael(self.waveform_dom_id, self.size_x, self.size_y + 16);

        self.el_background = this.r.rect(0, 0, self.size_x, self.size_y).attr({ stroke: "none", fill: self.waveform_fill });
        self.el_buffer = this.r.rect(0, 0, 0, self.size_y).attr({ stroke: "none", fill: self.waveform_fill });
        if(waveform_image) {
            self.el_waveform = this.r.image(waveform_image, 0, 0, 830, self.size_y);
        }
        self.el_indicator = this.r.rect(-10, 0, 2, self.size_y).attr({ stroke: "none", fill: '#00bb00' });

        // self.set_envelope();

    };


    this.init_markers = function (sections) {

        debug.debug('init_markers:', sections)

        if (sections.length > 1) {

            $(sections).each(function (i, section) {
                debug.debug('section', section);

                var pos_x = section.start / self.item.duration * 1000 * self.size_x;

                var width_x = section.duration / self.item.duration * 1000 * self.size_x;

                var height = 10;


                self.r.rect(pos_x, 90 - height, 1, height).attr({ stroke: "none", fill: '#63c', 'fill-opacity': 0.8 });

                self.r.rect(pos_x + 1, 90 - height, width_x - 1, height).attr({ stroke: "none", fill: '#63c', 'fill-opacity': 0.3 })
                    .mouseover(function () {
                        this.animate({"fill-opacity": .55, y: 0, height: 90}, 100);
                    })
                    .mouseout(function () {
                        this.animate({"fill-opacity": .3, y: 90 - height, height: 10}, 100);
                    })
                    .click(function (e) {
                        e.stopPropagation();
                        var el = this;
                        var pos_x = el.attrs.x - 1;
                        var pos = Number(pos_x / self.size_x * self.item.duration / 1000 - 1);
                        if (pos < 0) {
                            pos = 0;
                        }
                        self.player.seek(pos);

                    });

            });

        }


    };


    this.update = function (aplayer) {
        // debug.debug(aplayer);

        // check if current media is playing
        if (aplayer.states && aplayer.states.uuid && aplayer.states.uuid == self.item.uuid) {

            //debug.debug(aplayer);
            self.player = aplayer.player;
            self.aplayer_states = aplayer.states;

            var pos_x = self.size_x / 100 * aplayer.states.position_rel;

            //debug.debug(pos_x);

            self.el_indicator.attr({ x: pos_x + 'px' });
        }


    }


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




