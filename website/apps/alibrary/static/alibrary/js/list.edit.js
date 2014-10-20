/*
 * LISTEDIT
 * provides ui functionality for merge, delete etc
 */

/* core */


ListEditUi = function () {

    var self = this;

    this.ct = false;
    this.item_ids = [];
    this.selected = false;


    this.current_data = {
        item_type: null,
        item_id: null,
        provider: null,
        query: null,
        uri: null
    };

    this.dialog_window = false;


    this.init = function () {


        self.bindings();
        self.iface();
    };

    this.iface = function () {
    };

    this.bindings = function () {

        // lookup providers
        var container = $('.action-group');

        $(container).on('click', "li.action a:not('.disabled')", function (e) {
            e.preventDefault();
            var action = $(this).data('action');
            var ct = $(this).data('ct');
            self.ct = ct;

            switch (action) {
                case 'merge':
                    self.merge_items_dialog();
                    break;
                default:
                    //alert('nothing to do...')
            }

        });


        $('#merge_dialog_container .item').live('mouseover', function () {
            $(this).addClass('hover');
        });

        $('#merge_dialog_container .item').live('mouseout', function () {
            $(this).removeClass('hover');
        });

        $('#merge_dialog_container .item').live('click', function () {

            $('#merge_dialog_container .item').removeClass('selected master slave');
            $(this).addClass('selected master');
            $('#merge_dialog_container .item').not($(this)).addClass('slave');

            self.selected = $(this).data('id');

            debug.debug('selected id:', self.selected)

        });


        $('#merge_dialog_container .action a').live('click', function (e) {
            e.preventDefault();
            var action = $(this).data('action');

            if (action == 'confirm') {

                var data = {
                    item_ids: self.item_ids,
                    item_type: self.ct,
                    master_id: self.selected
                }

                if(!self.selected) {
                    alert('Selection required');
                    return false;
                }

                debug.debug('local', data);

                Dajaxice.alibrary.merge_items(function (data) {
                    debug.debug('remote', data);
                    try {
                        var api = self.dialog_window.qtip('api');
                        api.destroy();
                    } catch (e) {
                    }
                    if(data.status) {
                        document.location.reload();
                    } else {
                        alert(data.error);
                    }
                }, data);

            }
            if (action == 'cancel') {
                try {
                    var api = self.dialog_window.qtip('api');
                    api.destroy();
                } catch (e) {
                }
            }


        });


    };


    // collect all items with 'selected' state
    this.get_selection = function () {

        var item_ids = [];
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });

        return item_ids;

    };


    this.merge_items_dialog = function () {

        self.item_ids = [];

        self.item_ids = this.get_selection();
        debug.debug('ids:', self.item_ids);
        var data = {
            item_ids: self.item_ids,
            item_type: self.ct
        }

        // create dialog
        self.merge_dialog();

        // set it's content
        self.merge_dialog_update(data);


    };


    /***************************************************************************************
     * Dialog
     ***************************************************************************************/

    this.merge_dialog = function () {


        try {
            var api = self.dialog_window.qtip('api');
            api.destroy();
        } catch (e) {
        }


        self.dialog_window = $('<div />').qtip({
            content: {
                text: function (api) {
                    return '<div id="merge_dialog_container">loading</div>'
                }
            },
            position: {
                my: 'center',
                at: 'center',
                target: $(window)
            },
            show: {
                ready: true,
                modal: {
                    on: true,
                    blur: true
                }
            },
            hide: false,
            style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded popup-merge',
            events: {
                render: function (event, api) {
                    $('a.btn', api.elements.content).click(api.hide);
                }
            }
        });


    };


    this.merge_dialog_update = function (data) {


        // not so nice, but have to map type as names differ in api
        var item_type = data.item_type;
        var _item_type = item_type;

        if(_item_type == 'media') {
            _item_type = 'track';
        }

        var url = '/api/v1/' + _item_type + '/';
        var query = '?id__in=' + data.item_ids.join(',');

        $.get(url + query, function (data) {
            debug.debug(data);
            data.item_type = item_type;
            var html = nj.render('alibrary/nj/merge/merge_dialog.html', data);
            setTimeout(function () {
                $('#merge_dialog_container').html(html);
            }, 100)

        });

    };

    /***************************************************************************************
     * Utils & helpers
     ***************************************************************************************/


};

// should be called from corresponding place, with 'ctype' etc
// list_edit.ui = new ListEditUi();

