/*
 * very hackish. rather pre-alpha...
 */

PlaylistEditorUpload = function () {

    var self = this;

    this.fileupload_options = false
    this.api_url;

    this.uploaded = [];


    this.init = function () {

        self.fileupload = $('#fileupload');
        self.fileupload.fileupload('option', self.fileupload_options);
        this.bindings();

    };

    this.bindings = function () {


        self.fileupload.bind('fileuploaddone', function (e, data, whatever) {

            // console.log(data.result)

            var item = data.result;

            $('#playlist_editor_upload').append('<div id="' + item.uuid + '"></div>');

            var ifa = new ImportfileApp;
            ifa.local_data = item;
            ifa.container = $('#' + item.uuid);
            ifa.api_url = item.resource_uri;
            ifa.importer = self;

            ifa.update_callback = self.if_callback;

            ifa.init(true);


        });

    };

    this.if_callback = function (data) {

        //console.log('this.if_callback');
        //console.log(data);

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
                        debug.debug('created item:', item);
                        //data = data;
                        var html = '<div class="temporary item editable" id="playlist_item_' + item.id + '" data-uuid="' + item.uuid + '"><i class="icon-time icon-2x"></i>Computing waveform</div>'
                        $('#playlist_editor_list').append(html);

                        // reset
                        $('input', $('#playlist_editor_search')).val('');
                        $('.result', $('#playlist_editor_search')).html('');

                        setTimeout(function () {
                            alibrary.playlist_editor.reorder();
                        }, 10000)

                    }
                });
            }


        }
    }

};
