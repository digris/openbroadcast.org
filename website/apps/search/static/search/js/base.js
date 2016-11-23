;
var SearchApp = function () {
    var self = this;
    this.debug = false;
    this.base_url = '/api/v1/search/';
    this.input_container;
    this.results_container;

    this.search_mode = false;

    this.keyup_delay = 300;

    this.next_url = null;
    this.lock = false;

    this.current_request = null;

    this.q = null;

    this.ctypes = [
        'alibrary.release',
        'alibrary.artist',
        'alibrary.media'
    ];

    this.selected_ctypes = [];

    this.loading_template = '<div class="loading"><i class="icon icon-spinner icon-spin"></i><p>Loading Results</p></div>';

    this.bindings = function () {

        /*
         * handle query input
         */
        self.input_container.on('keyup', function (e) {

            console.debug('kc:', e.keyCode);

            e.preventDefault();

            if(e.keyCode != 27) {
                self.set_query($(this).val());

                if(e.keyCode != 32) {
                    delay(function () {
                        self.load()
                    }, self.keyup_delay);
                }

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
                    self.load_next();
                }
            }
        });



        /*
         * key bindings
         */
        $(document).on('keydown', function (e) {

            if(self.search_mode && e.keyCode == 27) {
                self.exit_search_mode();
                return;
            }


            // only listen to shift-+ x events
            if (e.shiftKey) {
                //e.preventDefault();
                if (self.debug) {
                    console.log('Shift + ', e.keyCode, '-', e.key);
                }
                switch (e.keyCode) {
                    case 32: // 'space'
                        e.preventDefault();
                        if(self.search_mode) {
                            self.input_container.focus();
                        } else {
                            self.enter_search_mode();
                        }
                        break;
                    // case 65: // 'a'
                    //     self.toggle_ctype('alibrary.artist');
                    //     break;
                    // case 82: // 'r'
                    //     self.toggle_ctype('alibrary.release');
                    //     break;
                    // case 84: // 't'
                    //     self.toggle_ctype('alibrary.media');
                    //     break;
                }


            }
        });


    };

    this.enter_search_mode = function() {
        if (self.debug) {
            console.log('enter search mode');
        }
        self.search_mode = true;
        self.input_container.val('');
        self.results_container.html('');
        $('body').addClass('global-search');
        self.input_container.focus();
    };

    this.exit_search_mode = function() {
        if (self.debug) {
            console.log('exit search mode');
        }
        self.search_mode = false;
        self.input_container.val('');
        self.results_container.html('');
        $('body').removeClass('global-search');
    };




    this.set_query = function (q) {

        self.input_container.val(q);

        if(q.length < 3) {
            self.clear_results();
            //return;
        }

        //History.replaceState({q: q}, null, '?q=' + q);
        self.q = q.trim();
    };

    this.toggle_ctype = function (ct) {

        if (ct == 'all') {
            if (self.selected_ctypes.length > 0) {
                self.selected_ctypes = [];
                self.set_ctypes();
                $(this).addClass('selected');
                self.load();
            }
            return;
        }

        var idx = $.inArray(ct, self.selected_ctypes);
        if (idx == -1) {
            self.selected_ctypes.push(ct);
        } else {
            self.selected_ctypes.splice(idx, 1);
        }

        self.set_ctypes();
        self.load();

    };

    this.set_ctypes = function () {

        var ctypes = self.selected_ctypes;

        console.log(ctypes);

        self.scope_container.find('a').removeClass('selected');

        if (self.selected_ctypes.length < 1) {
            self.scope_container.find('a[data-ct="all"]').addClass('selected')
        }


        $.each(self.selected_ctypes, function (i, el) {
            self.scope_container.find('a[data-ct="' + el + '"]').addClass('selected')
        });

    };

    this.load = function () {

        var q = self.q;
        var ctypes = self.selected_ctypes;

        if (!q) {
            return;
        }

        if (self.current_request) {
            self.current_request.abort();
        }

        if (self.debug) {
            console.log('search with query:', q);
        }

        if (q.length < 3) {
            self.clear_results();
            return;
        }


        self.results_container.html(self.loading_template);

        var url = self.base_url + '?q=' + q;
        if (ctypes.length > 0) {
            url += '&ct=' + ctypes.join(':');
        }

        self.current_request = $.get(url, function (data) {
            var results_html = '';
            $.each(data.objects, (function (i, object) {
                var d = {
                    object: object,
                    q: self.q
                };
                results_html += nj.render('search/nj/result.default.html', d);
            }));
            self.next_url = data.meta.next;
            self.results_container.html(results_html);

            self.lock = false;
            self.highlight();

        });

    };

    this.load_next = function () {

        if (!self.next_url) {
            return;
        }

        if (self.current_request) {
            self.current_request.abort();
        }

        self.results_container.append(self.loading_template);

        self.current_request = $.get(self.next_url, function (data) {
            var results_html = '';
            $.each(data.objects, (function (i, object) {
                var d = {
                    object: object,
                    q: self.q
                };
                results_html += nj.render('search/nj/result.default.html', d);
            }));
            self.next_url = data.meta.next;
            self.results_container.html(self.results_container.html() + results_html);

            $('.loading', self.results_container).remove();

            self.lock = false;
            self.highlight();

        });

    };

    this.highlight = function () {

        self.results_container.removeHighlight();
        if (!self.q) {
            return;
        }

        $.each(self.q.split(' '), function (i, el) {

            console.debug(el);

            self.results_container.highlight(el);

        })

    };


    this.clear_results = function () {
        self.results_container.html('');
    };

    this.init = function () {

        if (self.debug) {
            console.debug('SearchApp - init');
        }

        self.input_container = $('#search_input');
        self.scope_container = $('#search_scope');
        self.results_container = $('#search_results');

        // load query from url if available
        var q = $.url().param('q');
        if (q !== undefined) {
            self.set_query(q);
            self.load();
        }

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