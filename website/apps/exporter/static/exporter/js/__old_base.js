/*
 * EXPORTER
 */

/* core */


ExporterUi = function () {

    var self = this;

    this.interval = false;
    this.interval_loops = 0;
    this.interval_duration = 5000;
    this.api_url = false;

    this.dom_id = 'export_list_holder';
    this.dom_element;

    this.current_data = new Array;

    this.init = function () {

        debug.debug('exporter: init');
        debug.debug(self.api_url);

        this.dom_element = $('#' + this.dom_id);

        self.iface();
        self.bindings();

        // set interval and run once
        self.set_interval(self.run_interval, self.interval_duration);
        self.run_interval();

    };

    this.iface = function () {
        // this.floating_sidebar('lookup_providers', 120)
    };

    this.bindings = function () {


        // list items (on exporter screen)
        $('.action.download > a', self.dom_element).live('click', function (e) {
            e.preventDefault();

            if ($(this).parents('.item').hasClass('done')) {
                var url = $(this).data('url');
                // alert(url);
                // $.get(url);
                window.location.href = url;
            }
            ;

            if ($(this).parents('.item').hasClass('downloaded')) {

                // alert('already downloaded');
                var dialog = {
                    title: 'Error',
                    text: 'Already downloaded.',
                }
                util.dialog.show(dialog);

            }
            ;

        });

    };

    // interval
    this.set_interval = function (method, duration) {
        self.interval = setInterval(method, duration);
    };
    this.clear_interval = function (method) {
        self.interval = clearInterval(method);
    };

    this.run_interval = function () {
        self.interval_loops += 1;

        // Put functions needed in interval here
        self.update_exports();

    };

    this.update_exports = function () {

        $.getJSON(self.api_url, function (data) {
            self.update_exports_callback(data);
        });

    };
    this.update_exports_callback = function (data) {
        debug.debug(data);
        self.update_list_display(data);
    };

    this.update_list_display = function (data) {

        var status_map = new Array;
        status_map[0] = 'init';
        status_map[1] = 'done';
        status_map[2] = 'ready';
        status_map[3] = 'progress';
        status_map[4] = 'downloaded';
        status_map[99] = 'error';

        for (var i in data.objects) {

            var item = data.objects[i];
            var target_element = $('#export_' + item.id);

            item.status_key = status_map[item.status];

            if (item.status > -1) {

                if (item.id in self.current_data) {
                    self.current_data[item.id] = item;
                    debug.debug('item already present');

                    if (item.status != target_element.attr('data-last_status')) {
                        debug.debug('status change detected');

                        var html = ich.tpl_export({object: item});

                        html.attr('data-last_status', item.status);
                        target_element.replaceWith(html);
                    }

                } else {

                    var html = ich.tpl_export({object: item});
                    html.attr('data-last_status', item.status);
                    self.dom_element.prepend(html);

                    self.current_data[item.id] = item;
                }

            }

        }

    };


};

/*
 * exporter app - use this on listviews
 */
ExporterApp = (function () {

    var self = this;
    this.api_url = '/api/v1/export/'


    this.init = function () {
        debug.debug('ExporterApp: init');
        self.bindings();
    };

    this.bindings = function () {


        //////////////////////////////////////////////////////
        // "REAL" VERSION
        // using data- attributes
        //////////////////////////////////////////////////////
        $('.listview').on('click', 'a[data-action="download"]', function(e) {

            e.preventDefault();

            var item_type = $(this).data('ct');
            var item_id = $(this).data('id');
            var format = 'mp3';

            /*
             *  The controller takes a list of items as argument 'items'
             *  So the same api methods can also be used to implement download
             *  of multiple items at once. here we just pack this single item
             *  into an object
             */

            items = new Array;
            items.push({item_type: item_type, item_id: item_id, format: format});

            self.queue(items, false);
        });






        // handling of 'downloadables' & resp. queues
        // for single elements (through href/class)

        //////////////////////////////////////////////////////
        // LEGACY VERSION
        // using href
        //////////////////////////////////////////////////////
        $('.downloadable.queue').live('click', function (e) {

            e.preventDefault();

            // href is eg: "#release:324:flac"
            var action = $(this).attr('href').substr(1).split(':');

            var item_type = action[0];
            var item_id = action[1];
            var format = action[2];

            /*
             *  The controller takes a list of items as argument 'items'
             *  So the same controller can also be used to implement download
             *  of multiple items at once. we here just pack this single item
             *  into an object
             */

            items = new Array;
            items.push({item_type: item_type, item_id: item_id, format: format});

            self.queue(items, false);

        });

        /*
         * Download multiple items
         */
        $('.action.selection_download a').live('click', function (e) {

            var item_type = $(this).attr('href').substring(1);
            // item_type = 'release';

            items = new Array;
            $('.list_body_row.selection').each(function (index) {
                var item_id = $(this).attr('id').split("_").pop();
                items.push({item_type: item_type, item_id: item_id, format: 'mp3'});

                if (base.ui.use_effects) {
                    $(this).effect("transfer", { to: "#nav_sub-content li a.downloads" }, 300);
                }

            });

            self.queue(items, false);

            return false;
        });

    };


    this.queue = function (items, redirect) {

        var objects;
        var export_session;

        // try to get an open (status 0) export
        jQuery.ajax({
            url: self.api_url + '?status=0',
            success: function (data) {
                objects = data.objects;
            },
            async: false
        });


        // if none available: > create
        if (objects.length < 1) {
            jQuery.ajax({
                url: self.api_url,
                type: 'POST',
                data: JSON.stringify({filename: 'export - init'}),
                dataType: "json",
                contentType: "application/json",
                processData: false,
                success: function (data) {
                    debug.debug(data);
                    export_session = data;
                },
                async: false
            });
        } else {
            export_session = objects[0];
        }

        debug.debug('export session:', export_session);

        // add export-items
        for (i in items) {
            var item = items[i];

            debug.debug('exporter item:', item);

            var data = {
                // export_session: {'pk': export_session.id },
                export_session_id: export_session.id,
                item: item
            }

            jQuery.ajax({
                url: '/api/v1/exportitem/',
                type: 'POST',
                data: JSON.stringify(data),
                dataType: "json",
                contentType: "application/json",
                processData: false,
                success: function (data) {
                    debug.debug(data);
                    // export_session = data;
                },
                async: false
            });


        }

        // run the queue
        self.run(export_session);

        /**/






        // TODO: refactor dependency
        base.ui.ui_message('Download queued', 10000);


    };

    this.run = function (export_session) {
        jQuery.ajax({
            url: export_session.resource_uri,
            type: 'PATCH',
            data: JSON.stringify({status: 2}),
            dataType: "json",
            contentType: "application/json",
            processData: false,
            success: function (data) {
                debug.debug('queue:', data);
                export_session = data;
                if (redirect) {
                    window.location.href = export_session.download_url;
                }
            },
            async: true // this is the processing one - could take some time.
        });
    };

});