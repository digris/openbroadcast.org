/*
 * EXPORTER
 */

/* core */


ExporterMain = function () {

    var self = this;
    this.api_url = false;

    this.dom_id = 'export_list_holder';
    this.dom_element;
    this.toc_accepted = false;
    this.pushy_key;

    this.export_items = [];

    this.init = function () {

        debug.debug('exporter: init');
        debug.debug(self.api_url);

        this.dom_element = $('#' + this.dom_id);

        self.iface();
        self.bindings();

        self.load();

        pushy.subscribe(self.pushy_key, function () {
            self.load()
        });

    };

    this.iface = function () {
        // this.floating_sidebar('lookup_providers', 120)
    };

    this.bindings = function () {


    };


    this.load = function () {

        $.getJSON(self.api_url, function (data) {
            self.display(data);
        });

    };


    this.display = function (data) {

        $(data.objects).each(function (i, item) {

            if (!(item.uuid in self.export_items)) {
                var export_item = new ExporterItem;
                export_item.local_data = item;
                export_item.exporter_app = self;
                export_item.container = self.dom_element;
                export_item.api_url = item.resource_uri;
                export_item.init(true);
                self.export_items[item.uuid] = export_item;
            } else {
                debug.debug('Item exists on stage');
            }

            // $('#' + item.uuid).removeClass('delete-flag');

        });

    };


};


ExporterItem = function () {

    var self = this;
    this.api_url;
    this.container;
    this.dom_element = false;

    this.exporter_app;
    this.offset;

    this.local_data = false;

    this.init = function (use_local_data) {
        debug.debug('ExporterItem - init');
        self.load(use_local_data);
        pushy.subscribe(self.api_url, function () {
            self.load()
        });
    };

    this.load = function (use_local_data) {
        debug.debug('ExporterItem - load');

        if (use_local_data) {
            debug.debug('ExporterItem - load: using local data');
            self.display(self.local_data);
        } else {
            debug.debug('ExporterItem - load: using remote data');
            var url = self.api_url;
            $.get(url, function (data) {
                self.local_data = data;
                self.display(data);
            })
        }
    };

    this.bindings = function () {


        $(self.dom_element).on('click', 'a[data-action="download"]', function (e) {
            e.preventDefault();
            var download_url = self.local_data.download_url;


            if(!self.exporter_app.toc_accepted) {
                alert('You must accept the terms and conditions in order to download.');
                return;
            }

            if (self.local_data.status == 1) {
                window.location.href = download_url;
            }


            // TODO: allow multiple downloads?
            if (self.local_data.status == 4) { // 4: downloaded
                window.location.href = download_url;

                var dialog = {
                    title: 'Error',
                    text: 'Already downloaded.'
                }
                // util.dialog.show(dialog);

            }


        });


        $(self.dom_element).on('click', 'a[data-action="delete"]', function (e) {
            e.preventDefault();
            $.ajax({
                url: self.api_url,
                type: 'DELETE'
            }).done(function () {
                    self.dom_element.fadeOut(300)
                });
        });
    };


    this.display = function (data) {

        debug.debug('ExporterItem - display');
        debug.debug(data);

        // not so nice.. but for the moment...
        var status_map = new Array;
        status_map[0] = 'init';
        status_map[1] = 'done';
        status_map[2] = 'ready';
        status_map[3] = 'progress';
        status_map[4] = 'downloaded';
        status_map[99] = 'error';

        data.status_display = status_map[data.status]


        var html = nj.render('exporter/nj/export.html', { object: data });

        if (!self.dom_element) {
            console.log('create:', data);
            self.container.prepend(html);
            self.dom_element = $('#' + data.uuid, self.container);
        } else {
            $(self.dom_element).replaceWith(html);
            self.dom_element = $('#' + data.uuid, self.container);
        }

        self.bindings();

    };

};


/*
 * exporter app - use this on listviews
 */
ExporterApp = (function () {

    var self = this;
    this.api_url;


    this.init = function () {
        debug.debug('ExporterApp: init');
        self.bindings();
    };

    this.bindings = function () {

        // prevent on disabled TODO: maybe do globally
        /**/
        $('body').on('click', 'a[data-action].disabled', function (e) {
            e.preventDefault();
            e.stopPropagation();
        });


        // Download multiple items
        $('.action-group').on('click', 'a[data-action="download"].selection-any:not(".disabled")', function (e) {

            e.preventDefault();
            e.stopPropagation();

            // var item_type = $(this).data('ct'); // Moved - type should be taken from selected items ct
            var format = 'mp3';

            items = new Array;
            $('.list_body_row.selection').each(function (index) {
                var item_id = $(this).data('id');
                var item_type = $(this).data('ct');
                items.push({item_type: item_type, item_id: item_id, format: format});


                if (base.ui.use_effects) {
                    // $(this).effect("transfer", { to: "#nav_sub-content li a.downloads" }, 300);
                }

            });

            self.queue(items, false);
        });


        //////////////////////////////////////////////////////
        // Download single item
        // "REAL" VERSION
        // using data- attributes
        //////////////////////////////////////////////////////
        $('.listview , .action-group').on('click', 'a[data-action="download"]:not(".selection-any"):not(".disabled")', function (e) {

            e.preventDefault();
            //e.stopPropagation();


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

        var result = self.run(export_session, redirect);










    };

    this.run = function (export_session, redirect) {

        var status;
        var message;

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

                status = true;

                if (redirect) {
                    window.location.href = export_session.download_url;
                }

                base.ui.ui_message('Download queued', 10000);
            },
            error: function (a,b,c) {
                console.log(a,b,c)
                //alert(c);
                alert(a.responseText)

            },
            async: true // this is the processing one - could take some time.
        });

        return status;


    };

});