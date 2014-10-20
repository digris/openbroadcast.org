IstatsApp = function () {

    var self = this;
    this.api_url;
    this.dom_id = 'istats_container';
    this.dom_element;

    this.init = function () {
        debug.debug('IstatsApp - init');
        self.dom_element = $('#' + self.dom_id);

        setInterval(function(){
            self.load();
        }, 60000);

        self.load();
    };

    this.load = function() {
        $.get(self.api_url, function(data) {
            self.display(data);
        })
    };


    this.display = function(data) {

        debug.debug('load')

        d = {
            objects: data
        }


        var html = nj.render('istats/nj/server.html', d);
        self.dom_element.html(html)
    };



}; 	