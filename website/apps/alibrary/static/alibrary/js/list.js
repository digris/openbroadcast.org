/*
 * LISTEDIT
 * provides ui functionality for merge, delete etc
 */

/* core */


dw = false


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
                case 'reassign':
                    self.reassign_items();
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

                // display processing message

                try {
                    var api = self.dialog_window.qtip('api');
                    api.set('content.text', nj.render('alibrary/nj/merge/merge_dialog_progress.html'));
                } catch (e) {
                }


                /**/
                Dajaxice.alibrary.merge_items(function (data) {
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


    /***************************************************************************************
     * Merge function
     * TODO: this should be refactored to a more generic way
     ***************************************************************************************/
    this.merge_items_dialog = function () {

        self.item_ids = [];

        self.item_ids = this.get_selection();
        var data = {
            item_ids: self.item_ids,
            item_type: self.ct
        }

        // create dialog
        self.merge_dialog();

        // set it's content
        self.merge_dialog_update(data);


    };

    this.merge_dialog = function () {


        try {
            var api = self.dialog_window.qtip('api');
            api.destroy();
        } catch (e) {
        }


        self.dialog_window = $('<div />').qtip({
            content: {
                text: function (api) {
                    return '<div id="merge_dialog_container"><div class="loading-placeholder"><i class="icon-spinner icon-spin icon-large"></i> loading</div></div>'
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
            style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded  popup-actions popup-merge',
            events: {
                render: function (event, api) {
                    $(this).on('click', 'a[data-action="exit"]', function(e){
                        api.destroy();
                    });
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

        var url = '/api/v1/library/' + _item_type + '/';
        var query = '?limit=120&id__in=' + data.item_ids.join(',');

        $.get(url + query, function (data) {
            data.item_type = item_type;
            var html = nj.render('alibrary/nj/merge/merge_dialog.html', data);
            setTimeout(function () {
                $('#merge_dialog_container').html(html);
            }, 100)
        });

    };






    /***************************************************************************************
     * Re-assign function
     * TODO: this should be refactored to a more generic way
     ***************************************************************************************/

    this.reassign_items = function () {

        self.item_ids = [];
        self.item_ids = this.get_selection();
        var data = {
            item_ids: self.item_ids,
            item_type: self.ct
        }

        self.reassign_dialog();

    };


    this.reassign_dialog = function () {

        try {
            var api = self.dialog_window.qtip('api');
            api.destroy();
        } catch (e) {
        }

        self.dialog_window = $('<div />').qtip({
            content: {
                text: function (api) {
                    return nj.render('alibrary/nj/reassign/reassign_dialog.html', {});
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
            style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded  popup-actions popup-reassign',
            events: {
                render: function (event, api) {
                    var container = $(this);

                    setTimeout(function(){
                        $('input.query', container).focus();
                    }, 100)


                    $(this).on('click', 'a[data-action="exit"]', function(e){
                        api.destroy();
                    });

                    $(this).on('click', 'a[data-action="stay"]', function(e){
                        api.destroy();
                        document.location.reload();
                    });

                    $(this).on('click', 'a[data-action="continue"]', function(e){
                        api.destroy();
                        document.location = '/';
                    });

                    $(this).on('click', '.item', function(e){
                        $('.item', container).not(this).removeClass('selected');
                        if(!$(this).hasClass('selected')){
                            $(this).addClass('selected');
                        } else {
                          $(this).removeClass('selected');
                        };
                    });

                    $(this).on('keyup', 'input.query', function(e){

                        var el = $(this);
                        var q = $(this).val();
                        // catch enter
                        if (e.keyCode == 13 || e.keyCode == 9) {
                            var uri = util.uri_param_insert(window.location.href, 'q', q, true);
                            window.location = util.uri_param_insert(uri, 'page', 1, true);
                            return false;
                        }

                        // autocomplete
                        util.delay(function(){
                            self.reassign_autocomplete(container, q);
                        }, 200 );

                    });

                    $(this).on('click', 'a[data-action="confirm"]', function(e){


                        if($('.item', container).hasClass('selected')) {

                            var data = {
                                'release_id': $('.item.selected', container).data('id'),
                                'media_ids': self.item_ids
                            }
                        } else {
                            var query = $('input.query' ,container).val();
                            if(query.length < 3) {
                                alert('name too short');
                                return;
                            }
                            var data = {
                                'name': query,
                                'media_ids': self.item_ids
                            }
                        }

                        // lock ui
                        try {
                            var api = self.dialog_window.qtip('api');
                            api.set('content.text', nj.render('alibrary/nj/reassign/reassign_dialog_progress.html'));
                        } catch (e) {
                        }


                        Dajaxice.alibrary.reassign_items(function (data) {

                            // unlock ui
                            try {
                                //var api = self.dialog_window.qtip('api');
                               // api.destroy();
                            } catch (e) {
                            }


                            if(data.status) {
                                var html = nj.render('alibrary/nj/reassign/reassign_dialog_continue.html', data);
                                $('.qtip-content', container).html(html)

                            } else {
                                alert(data.error);
                            }
                        }, data);




                    });


                }
            }
        });

    };

    this.reassign_autocomplete = function(container, q) {

        var url = '/api/v1/library/release/autocomplete-name/'

        if (q.length >= 3) {
            $.get(url + '?q=' + q, function (data) {

                if(data.objects.length) {
                    var html = nj.render('alibrary/nj/reassign/reassign_dialog_search_result.html', data);
                    $('#search_result', container).html(html);
                } else {
                    $('#search_result', container).html('');
                }
            });
        } else {
            $('#search_result', container).html('');
        }

    };


    this.reassign_dialog_update = function (data) {


        // not so nice, but have to map type as names differ in api
        var item_type = data.item_type;
        var _item_type = item_type;

        if(_item_type == 'media') {
            _item_type = 'track';
        }

        var url = '/api/v1/library/' + _item_type + '/';
        var query = '?id__in=' + data.item_ids.join(',');

        $.get(url + query, function (data) {
            data.item_type = item_type;
            var html = nj.render('alibrary/nj/reassign/reassign_dialog.html', data);
            setTimeout(function () {
                $('#reassign_dialog_container').html(html);
            }, 100)

        });

    };



    /***************************************************************************************
     * Utils & helpers
     ***************************************************************************************/


};

// should be called from corresponding place, with 'ctype' etc
// list_edit.ui = new ListEditUi();



var RangeFilter = function() {
    var self = this;
    this.el;
    this.range = {
        'start': false,
        'end': false
    };

    this.init = function(el) {
        self.el = el;
        self.get_state();
        self.bindings();
    };

    this.get_state = function() {
        var params = $.url().param('releasedate');
        if (params != undefined) {
            params = params.split(':');
            if(params[0] && params[0].length == 10) {
                self.range.start = params[0];
            }
            if(params[1] && params[1].length == 10) {
                self.range.end = params[1];
            }

        } else {
            self.range.start = false;
            self.range.end = false;
        }

        self.update_display();
    };

    this.update_display = function() {

        var container = $('#releasedate_range_container', self.el);

        // hack - but needed for compatibility
        if(self.range.start || self.range.end) {
            container.addClass('minus');
            container.removeClass('plus');
        } else {
            container.addClass('plus');
            container.removeClass('minus');
        }

        // set values
        if(self.range.start) {
            $('[name="range-start"]', container).val(self.range.start.substr(0,4))
        } else {
            $('[name="range-start"]', container).val(false)
        }
        if(self.range.end) {
            $('[name="range-end"]', container).val(self.range.end.substr(0,4))
        } else {
            $('[name="range-end"]', container).val(false)
        }

    };

    this.update_query = function() {

        str_start = (self.range.start) ? self.range.start : '';
        str_end = (self.range.end) ? self.range.end : '';

        var url = $.insert_uri_param(window.location.href, 'releasedate', str_start + ':' + str_end, true);
        url = $.insert_uri_param(url, 'page', 1, true);

        window.location.href = url;

    };

    this.bindings = function(el) {

        // form elements
        $(self.el).on('change', 'select', function(e){

            var val = $(this).val();
            if($(this).attr('name') == 'range-start') {
                if(val && val != '') {
                    self.range.start = val + '-01-01';
                } else {
                    self.range.start = false;
                }

            }
            if($(this).attr('name') == 'range-end') {
                if(val && val != '') {
                    self.range.end = val + '-12-31';
                } else {
                    self.range.end = false;
                }
            }

            self.update_query();
        });

        // predefined selections
        $('#predefined_selector', self.el).on('click', 'a.preset', function(e){

            e.preventDefault();

            var range_start = $(this).data('range_start');
            var range_end = $(this).data('range_end');

            if(range_start != undefined) {
                self.range.start = range_start;
            } else {
                self.range.start = false;
            }

            if(range_end != undefined) {
                self.range.end = range_end;
            } else {
                self.range.end = false;
            }

            self.update_query();
        });



    };

};

$(function(){
    if($('#filterbox_holder-releasedate').length) {
        var rf = new RangeFilter();
        rf.init($('#filterbox_holder-releasedate'));
    }
});
