;
var SearchApp = function () {
    var self = this;
    this.debug = false;
    this.base_url = '/api/v1/search/';
    this.input_container;
    this.results_container;
    this.selected_result = null;
    this.autocomplete_timeout = false;



    this.search_mode = false;

    this.keyup_delay = 300;

    this.result_meta = {
        next_url: null
    };

    this.lock = false;

    this.current_request = null;

    this.q = null;

    this.ctypes = [
        'alibrary.release',
        'alibrary.artist',
        'alibrary.media',
        'profiles.profile'
    ];

    this.ctype_map = {
        'alibrary.release': {
            display_name: 'Release',
            keys: [
                [['p'], 'play'],
                [['q'], 'queue'],
                [['e'], 'edit view'],
                [['Enter'], 'detail view']
            ]
        },
        'alibrary.artist': {
            display_name: 'Artist',
            keys: [
                [['p'], 'play'],
                [['e'], 'edit view'],
                [['Enter'], 'detail view']
            ]
        },
        'alibrary.media': {
            display_name: 'Track',
            keys: [
                [['p'], 'play'],
                [['q'], 'queue'],
                [['a'], 'add to playlist'],
                [['e'], 'edit view'],
                [['Enter'], 'detail view']
            ]
        },
        // profiles
        'profiles.profile': {
            display_name: 'User',
            keys: [
                [['Enter'], 'detail view']
            ]
        }
    };

    this.selected_ctypes = [];

    this.loading_template = '<div class="loading"><i class="icon icon-spinner icon-spin"></i><p>Loading Results</p></div>';

    // references to platform apps
    this.collector;
    this.player;




    this.bindings = function () {


        /*
         * global key bindings
         * handle entering and exiting search mode
         */
        $(document).on('keydown', function (e) {

            // exit search mode on 'esc
            if (self.search_mode && e.keyCode == 27) {
                if (self.debug) {
                    console.debug('"esc" in active search mode -> exit search mode');
                }
                self.exit_search_mode();
                return;
            }

            // handle entering search mode & input focus
            if (e.shiftKey && e.keyCode == 32) {
                e.preventDefault();
                if (self.debug) {
                    console.log('Shift + ', e.keyCode, '-', e.key);
                }
                if (self.search_mode) {
                    if (self.debug) {
                        console.debug('"shift+s" in search mode. set focus to input if not already');
                    }
                    if (self.input_container.is(":focus")) {
                        if (self.debug) {
                            console.debug('search input already has focus');
                        }
                    } else {
                        if (self.debug) {
                            console.debug('set focus on search input');
                        }
                        e.preventDefault();
                        self.input_container.focus();
                    }
                } else {
                    if (self.debug) {
                        console.debug('"shift+s" without search mode. enter search mode');
                    }
                    e.preventDefault();
                    self.enter_search_mode();
                }
            }

            // listening for alt-+ x events (in search mode only)
            if (self.search_mode && e.altKey) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                switch (e.keyCode) {
                    case 65: // 'a'
                        self.toggle_ctype('alibrary.artist');
                        break;
                    case 82: // 'r'
                        self.toggle_ctype('alibrary.release');
                        break;
                    case 84: // 't'
                        self.toggle_ctype('alibrary.media');
                        break;
                }

            }

        });

        this.input_container.on('keyup', function (e) {


            // pass to keyboard navigation handler
            self.keyboard_result_selection(e);

            // handle keyborad navigation on result
            if(self.result_has_focus()) {
                self.keyboard_result_action(e);
            }

            var q = $(this).val();

            // check if the querystring actually did change, ignoring whitespace.
            if ($.trim(self.q) != $.trim(q)) {
                self.q = q;
                delay(function () {
                    self.search()
                }, 350);
            }

        });


        /*
         * prevent key input if a result has 'focus'
         */
        this.input_container.on('keydown', function (e) {

            if(self.result_has_focus()) {
                e.preventDefault();
                return;
            }
        });



        /*
         * handle ctype filters
         */
        self.scope_container.on('click', 'a', function (e) {
            e.preventDefault();
            self.toggle_ctype($(this).data('ct'));
        });


        /*
         * infinite scrolling
         */
        $(document).scroll(function (e) {
            if (element_in_scroll($('.search-results .item:last'))) {
                if (!self.lock) {
                    self.lock = true;
                    self.search_next();
                }
            }
        });


    };


    /*
     * enter search mode
     */
    this.enter_search_mode = function () {
        if (self.debug) {
            console.log('enter search mode');
        }
        self.search_mode = true;
        self.input_container.val('');
        self.clear_results();
        self.set_result_focus();
        $('body').addClass('global-search');
        $('body').animate({scrollTop: 0}, 200);
        self.input_container.focus();

    };

    /*
     * exit search mode
     */
    this.exit_search_mode = function () {
        if (self.debug) {
            console.log('exit search mode');
        }
        self.search_mode = false;
        self.input_container.val('');
        self.clear_results();
        self.set_result_focus();
        $('body').removeClass('global-search');
    };


    /*
     * check if a result has 'focus'
     */
    this.result_has_focus = function() {
        return $('.item.selected', self.results_container).length;
    };


    /*
     * handle cursor up/down for result selection
     */
    this.keyboard_result_selection = function (e) {

        var results = self.results_container.find('.item');
        var selected = -1;
        var can_next = false;
        var can_previous = false;

        if (results.length) {

            results.each(function (i, el) {
                if ($(el).hasClass('selected')) {
                    selected = i;
                }
            });

            if (selected < (results.length - 1)) {
                can_next = true;
            }

            if (selected < (results.length)) {
                can_previous = true;
            }

            if (e.keyCode == 38 && can_previous) {
                e.preventDefault();
                selected--;
                results.each(function (i, el) {
                    if (i == selected) {
                        $(el).addClass('selected')
                    } else {
                        $(el).removeClass('selected')
                    }
                });

            }

            if (e.keyCode == 40 && can_next) {
                e.preventDefault();
                selected++;
                results.each(function (i, el) {
                    if (i == selected) {
                        $(el).addClass('selected')
                    } else {
                        $(el).removeClass('selected')
                    }
                });

            }

            self.set_result_focus();

        }
    };


    /*
     * handle keyboard input for 'focused' result
     */
    this.keyboard_result_action = function (e) {

        var item = self.selected_result;

        if(item) {

            var key_map = self.ctype_map[item.ct].keys;

            // TODO: handle 'combo cases'
            var keys = [];
            $.each(key_map, function(i, el){
                keys.push(el[0][0])
            });

            if ($.inArray(e.key, keys) > -1) {
                e.preventDefault();

                // enter
                if(e.key == 'Enter') {
                    document.location.href = item.detail_uri;
                    return;
                }

                // e - edit
                if(e.key == 'e') {
                    document.location.href = item.edit_uri;
                    return;
                }

                // p - play
                if(e.key == 'p') {
                    self.player.play_in_popup(item.resource_uri, '_', 0, 'replace', false, item.ct.split('.')[0]);
                    $('.selected', self.results_container).effect( "transfer", { to: $( "#aplayer_inline" ) }, 300 );
                }

                // q - queue
                if(e.key == 'q') {
                    self.player.play_in_popup(item.resource_uri, '_', 0, 'queue', false, item.ct.split('.')[0]);
                    $('.selected', self.results_container).effect( "transfer", { to: $( "#aplayer_inline" ) }, 300 );
                }

                // a - add to playlist
                if(e.key == 'a') {
                    alibrary.collector.media_to_collect = [{id: item.id, uuid: item.uuid}];
                    alibrary.collector.dialogue(e)
                }

            }

        }

    };


    this.set_result_focus = function(clear) {

        var el_focus = false;
        var item = false;

        if(clear === undefined) {
            if($('.selected', self.results_container).length) {
                el_focus = self.results_container.find('.selected');
            }
        }

        // get data attributes for focused element
        if(el_focus) {
            item = $(el_focus).data();


            item = $.extend({}, item, self.ctype_map[item.ct]);


        }

        //console.info('result focus:', el_focus);

        self.selected_result = item;
        self.update_result_context(item);

    };



    // this.set_query = function (q) {
    //
    //     self.input_container.val(q);
    //
    //     if(q.length < 3) {
    //         self.clear_results();
    //         //return;
    //     }
    //
    //     //History.replaceState({q: q}, null, '?q=' + q);
    //     self.q = q.trim();
    // };

    this.toggle_ctype = function (ct) {

        var set_ctypes = function (ctypes) {
            self.scope_container.find('a').removeClass('selected');
            if (ctypes.length < 1) {
                self.scope_container.find('a[data-ct="all"]').addClass('selected')
            }
            $.each(ctypes, function (i, el) {
                self.scope_container.find('a[data-ct="' + el + '"]').addClass('selected')
            });
        };

        if (ct == 'all') {
            if (self.selected_ctypes.length > 0) {
                self.selected_ctypes = [];
                set_ctypes(self.selected_ctypes);
                $(this).addClass('selected');
                self.search();
            }
            return;
        }

        var idx = $.inArray(ct, self.selected_ctypes);
        if (idx == -1) {
            self.selected_ctypes.push(ct);
        } else {
            self.selected_ctypes.splice(idx, 1);
        }

        set_ctypes(self.selected_ctypes);
        self.search();

    };


    /*
     * default search (query & scope)
     */
    this.search = function () {

        var q = self.q;

        if (q.length < 3) {
            self.clear_results();
            return;
        }

        var ctypes = self.selected_ctypes;
        var url = self.base_url + '?q=' + q;
        if (ctypes.length > 0) {
            url += '&ct=' + ctypes.join(':');
        }

        self.api_request({
            url: url,
            beforeSend: function() {
                self.results_container.html(self.loading_template);
            }
        })

    };


    /*
     * 'endless' scrolling search (using 'next' from meta)
     */
    this.search_next = function () {

        var url = self.result_meta.next;

        if (!url) {
            return;
        }

        self.api_request({
            url: url,
            beforeSend: function() {
                self.results_container.append(self.loading_template);
            }
        })

    };

    /*
     * perform the actual ajax request on search api
     * options: jquery ajax options
     */
    this.api_request = function(options) {

        var defaults = {
            url: null,
            method: 'get',
            timeout: 5000,
            success: function(data) {
                var results_html = '';
                $.each(data.objects, (function (i, object) {
                    results_html += nj.render('search/nj/result.default.html', {object: object, q: self.q});
                }));
                self.results_container.html(self.results_container.html() + results_html);
                $('.loading', self.results_container).remove();

            }
        };

        // abort existing request
        if (self.current_request) {
            self.current_request.abort();
        }

        self.current_request = $.ajax($.extend({}, defaults, options));

        // global result handling
        self.current_request.success(function(data){
            self.result_meta = data.meta;
            self.highlight();
        });
        // global release lock
        self.current_request.complete(function(data){
            self.lock = false;
            self.update_summary_display();
            self.set_result_focus();
        });

    };

    this.highlight = function () {

        self.results_container.removeHighlight();
        if (!self.q) {
            return;
        }

        $.each(self.q.split(' '), function (i, el) {
            self.results_container.highlight(el);
        })

    };



    this.update_summary_display = function() {

        var container = self.summary_container.find('.result-meta-container');

        var html = nj.render('search/nj/result.meta.html', {meta: self.result_meta, q: self.q});
        container.html(html);

    };

    this.update_result_context = function(item) {

        var container = self.summary_container.find('.result-context-container');
        
        if(item) {
            var html = nj.render('search/nj/result.context.html', {object: item});
            container.html(html);
        } else {
            container.html('')
        }

    };


    this.clear_results = function () {
        self.results_container.html('');
        self.summary_container.find('.result-meta-container').html('');
    };

    this.init = function () {

        if (self.debug) {
            console.debug('SearchApp - init');
        }

        self.input_container = $('#search_input');
        self.scope_container = $('#search_scope');
        self.results_container = $('#search_results');
        self.summary_container = $('#search_summary');

         self.player = aplayer.base;



        // load query from url if available
        // var q = $.url().param('q');
        // if (q !== undefined) {
        //     self.set_query(q);
        //     self.search();
        // }

        self.bindings();
    };

};

var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

var element_in_scroll = function (el) {

    if (!el.length) {
        return false;
    }

    var top = $(window).scrollTop();
    var bottom = top + $(window).height();

    var el_top = el.offset().top;
    var el_bottom = el_top + el.height();

    return ((el_bottom <= bottom) && (el_top >= top));
};