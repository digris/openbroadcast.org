BackfeedUi = function () {

    var self = this;
    var post_url;
    var el;

    this.init = function () {
        console.log('BackfeedUi: init');
        self.el = $('.backfeed');
        self.bindings();
    };

    this.bindings = function () {
        console.log('BackfeedUi: bindings');

        // show/hide backfeed
        self.el.on('click', '.toggle > a', function (e) {
            e.preventDefault();
            $(this).parents('.backfeed').toggleClass('expanded');
        });


        // submit form
        self.el.on('click', 'form a.submit', function (e) {
            e.preventDefault();
            var form = $(this).parents('form');
            var data = form.serialize();
            console.log(data);

            $.ajax({
                url: self.post_url,
                type: "POST",
                data: data,
                success: function(response) {
                    console.log(response)

                    if(response.status == true) {
                        self.show_success('');
                    } else {
                        self.show_errors(response.errors)
                    }

                },
                error: function(e, x, t) {
                    console.log(e, x, t);
                }
            });

        });


    };

    this.show_success = function() {
        $('#backfeed_errors', self.el).hide();
        $('#backfeed_form', self.el).hide();
        $('#backfeed_success', self.el).show();
    };

    this.show_errors = function(errors) {

        $('input, textarea', self.el).removeClass('error');

        $('#backfeed_success', self.el).hide();
        $('#backfeed_errors', self.el).show();

        $.each(errors, function(k, v){
            $("[name='" + k + "']", self.el).addClass('error');

        });

    };


};

