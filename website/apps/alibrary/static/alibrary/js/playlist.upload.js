/*
 * very hackish. rather pre-alpha...
 */

PlaylistEditorUpload = function () {

    var self = this;

    this.fileupload_options = false
    this.api_url;
    this.pushy_paused = false;

    this.uploaded = [];


    this.init = function () {

        self.fileupload = $('#fileupload');
        self.fileupload.fileupload('option', self.fileupload_options);
        this.bindings();

    };

    this.bindings = function () {


        self.fileupload.bind('fileuploaddone', function (e, data) {

            var item = data.result;

            $('#playlist_editor_upload').append('<div id="' + item.uuid + '"></div>');

            var ifa = new ImportfileApp;
            ifa.local_data = item;
            ifa.container = $('#' + item.uuid);
            ifa.api_url = item.resource_uri;
            ifa.importer = self;

            ifa.update_callback = self.if_callback;

            ifa.init(true);
            ifa.bindings();


        });

    };

    this.if_callback = function (data) {

        if (data.status == 'done' || data.status == 'duplicate') {

            // if (!$.inArray(data.id, self.uploaded)) {
            if (! self.uploaded.indexOf(data.id) > -1) {
                self.uploaded.push(data.id);

                $.ajax({
                    url: self.api_url + 'collect/',
                    type: 'POST',
                    data: {
                        ids: [data.media.id].join(','),
                        ct: 'media'
                    },
                    dataType: "json",
                    contentType: "application/json",
                    success: function (data) {
                        var item = data.items.pop();

                        var html = '<div class="temporary item editable" id="playlist_item_' + item.id + '" data-uuid="' + item.uuid + '">Loading Data</div>'
                        $('#playlist_editor_list').append(html);

                        // reset
                        $('input', $('#playlist_editor_search')).val('');
                        $('.result', $('#playlist_editor_search')).html('');

                        setTimeout(function () {
                            alibrary.playlist_editor.reorder();
                        }, 100)

                    }
                });
            }


        }
    }
    this.lock_ui = function(lock) {
        if(lock) {
            $('#importer_ui_lock').show();
            //$('body').css('opacity', 0.5);
        } else {
            $('#importer_ui_lock').hide();
            //$('body').css('opacity', 1);
        }
    };

};
