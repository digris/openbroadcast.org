;
var SearchApp = function () {
    var self = this;
    this.debug = false;
    this.base_url = '/api/v1/search/';
    this.input_container;
    this.results_container;

    this.keyup_delay = 300;

    this.bindings = function () {

        self.input_container.on('keyup', function (e) {

            var q = $(this).val();

            delay(function () {
                self.search(q)
            }, self.keyup_delay);

        });

    };

    this.search = function (q) {

        if (self.debug) {
            console.log('search with query:', q);
        }

        if (q.length < 1) {
            self.clear_results();
            return;
        }

        var url = self.base_url + '?q=' + q;
        $.get(url, function (data) {

            self.results_container.html('');
            var results_html = '';

            $.each(data.objects, (function (i, object) {

                if (self.debug) {
                    console.debug(object);
                }
                var d = {
                    object: object,
                    q: q
                };

                var html = $(nj.render('search/nj/result.default.html', d));
                self.results_container.append(html.fadeIn(i * 100));


                //results_html += nj.render('search/nj/result.default.html', d);

            }));

            //self.results_container.html(results_html);

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
        self.results_container = $('#search_results');

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
