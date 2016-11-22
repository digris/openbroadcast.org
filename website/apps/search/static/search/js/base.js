;
var SearchApp = function () {
    var self = this;
    this.debug = false;
    this.base_url = '/api/v1/search/';
    this.input_container;
    this.results_container;
    this.keyup_delay = 300;

    this.next_url = null;
    this.lock = false;

    this.q = null;

    this.ctypes = [
        'alibrary.release',
        'alibrary.artist',
        'alibrary.media'
    ];

    this.selected_ctypes = [];

    this.bindings = function () {

        self.input_container.on('keyup', function (e) {

            self.set_query($(this).val());

            delay(function () {
                self.load()
            }, self.keyup_delay);

        });

        self.scope_container.on('click', 'a', function (e) {
            e.preventDefault();

            var ct = $(this).data('ct');

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

        });

        // scroll loader
        $(document).scroll(function (e) {


            console.debug('scroll');
            if (element_in_scroll($('.search-results .item:last'))) {
                console.debug('scroll - element_in_scroll!');
                if(!self.lock) {
                    self.lock = true;
                    self.load_next();
                }
            }
        });

    };

    this.set_query = function (q) {
        self.input_container.val(q);
        History.replaceState({q: q}, null, '?q=' + q);
        self.q = q;
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

        if (self.debug) {
            console.log('search with query:', q);
        }

        if (q.length < 1) {
            self.clear_results();
            return;
        }

        self.results_container.html('<div class="loading"><i class="icon icon-spinner icon-spin"></i></div>');

        var url = self.base_url + '?q=' + q;
        if (ctypes.length > 0) {
            url += '&ct=' + ctypes.join(':');
        }

        $.get(url, function (data) {
            var results_html = '';
            $.each(data.objects, (function (i, object) {
                var d = {
                    object: object,
                    q: q
                };
                results_html += nj.render('search/nj/result.default.html', d);
            }));
            self.next_url = data.meta.next;
            self.results_container.html(results_html);

            self.lock = false;

        });

    };

    this.load_next = function () {

        if(!self.next_url) {
            return;
        }

        $.get(self.next_url, function (data) {
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

            self.lock = false;

        });

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

    if(!el.length) {
        return false;
    }

    var top = $(window).scrollTop();
    var bottom = top + $(window).height();

    var el_top = el.offset().top;
    var el_bottom = el_top + el.height();

    return ((el_bottom <= bottom) && (el_top >= top));
};