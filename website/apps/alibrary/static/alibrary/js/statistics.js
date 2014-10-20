StatisticApp = function () {

    var self = this;

    //this.ct;
    //this.id;
    this.resource_uri;
    this.dom_id = 'statistics_container';
    this.loaded = false;
    this.loading = false;


    this.init = function () {
        console.log('StatisticApp: init', self.resource_uri);
    };


    this.show = function () {
        console.log('StatisticApp: load - loaded:', self.loaded);


        if (!self.loaded) {
            self.load();
        }

    };

    this.load = function () {

        var url = self.resource_uri + 'stats/';


        $.get(url, function (data) {
            console.log('response data:', data);

            // hard-code color indices to prevent them from shifting
            var i = 0;
            $.each(data, function (key, val) {
                val.color = i;
                ++i;
            });

            // insert checkboxes & bind click event
            var choice_container = $('#plot_choices');
            $.each(data, function (key, val) {
                choice_container.append("<li><input type='checkbox' name='" + key +
                    "' checked='checked' id='id" + key + "'></input>" +
                    "<label for='id" + key + "'>"
                    + val.label + "</label></li>");
            });
            $('input', choice_container).on('click', function (e) {
                self.plot(data);
            });

            self.loaded = true;
            self.plot(data);


            $('.message', $('#' + self.dom_id)).hide();


        });

    };

    this.plot = function (data) {


        var datasets = [];

        $('#plot_choices').find("input:checked").each(function () {
            var key = $(this).attr("name");
            if (key && data[key]) {
                datasets.push(data[key]);
            }
        });

        if (datasets.length > 0) {
            $.plot('#' + self.dom_id, datasets, {
                xaxis: {
                    mode: "time",
                    minTickSize: [1, "month"]
                },
                grid: {
                    show: true,
                    aboveData: true,
                    color: '#999999',
                    backgroundColor: '#ffffff',
                    margin: 0,
                    borderWidth: 0,
                    borderColor: null,
                    clickable: true,
                    hoverable: true,
                    autoHighlight: true

                },
                legend: {

                },
                series: {
                    lines: { show: true, fill: true},
                    points: { show: false, fill: false }
                },
                colors: ["#47248F", "#00BB00", "#00ffff"],
                crosshair: {
                    mode: "x"
                }
            });
        }
        ;


    };


};