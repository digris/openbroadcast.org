;
var SearchApp = function () {
    var self = this;
    this.debug = false;
    this.base_url = '/api/v1/search/';
    this.input_container;
    this.results_container;

    this.bindings = function () {

        self.input_container.on('keyup', function(e){

            var q = $(this).val();
            self.search(q);
            
        });


    };

    this.search = function (q) {

        if(q.length < 3) {
            return;
        };

        var url = self.base_url + '?q=' + q;
        $.get(url, function(data){

            self.results_container.html('');
            var results_html = '';

            $.each(data.objects, (function(i, object){

                console.debug(object)
                var d = {
                    object: object
                };
                results_html += nj.render('search/nj/result.default.html', d);

            }));

            self.results_container.html(results_html);



        });


    };





    this.init = function () {

        if(self.debug) {
            console.debug('SearchApp - init');
        }
        
        self.input_container = $('#search_input');
        self.results_container = $('#search_results');


        self.bindings();
    };

};
